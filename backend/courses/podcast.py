import openai
import random
from openai import OpenAI
import os
from django.conf import settings
from django.db.models import Count, Q
from courses.models import Course, Module, Lesson, LessonContent

# Use API key from settings instead of hardcoding
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_course_content(course_id: int):
    """Extract useful content from a course to generate a podcast"""
    try:
        course = Course.objects.get(id=course_id)
        
        # Get modules and lessons
        modules = Module.objects.filter(course=course).order_by('order')
        
        # Gather key information about the course
        course_data = {
            "title": course.title,
            "description": course.description,
            "category": course.category.name if course.category else "Uncategorized",
            "tags": course.tags,
            "modules": []
        }
        
        # Get key points from each module and its lessons
        for module in modules:
            module_data = {
                "title": module.title,
                "description": module.description,
                "lessons": []
            }
            
            lessons = Lesson.objects.filter(module=module).order_by('order')
            for lesson in lessons:
                try:
                    content = LessonContent.objects.get(lesson=lesson)
                    lesson_data = {
                        "title": lesson.title,
                        "type": lesson.get_content_type_display(),
                        "duration": lesson.estimated_duration,
                        "content_preview": content.text_content[:200] + "..." if content.text_content else "[No text content]"
                    }
                    module_data["lessons"].append(lesson_data)
                except LessonContent.DoesNotExist:
                    pass
            
            course_data["modules"].append(module_data)
        
        return course_data
    
    except Course.DoesNotExist:
        return None

def generate_podcast_script(course_data, style="fun"):
    """Generate a podcast script based on course data"""
    
    # Define different podcast styles
    styles = {
        "fun": """
            Make this extremely fun, casual and entertaining. Include jokes, puns, and funny analogies.
            The hosts should have distinct personalities - Alex is enthusiastic and energetic, while Nova is witty and slightly sarcastic.
            Include at least 3 funny jokes or puns related to the course material.
            Use casual language and pop culture references that would appeal to younger listeners.
            Include a "Fun Fact Break" section where you share an unexpected or amusing fact related to the topic.
        """,
        "storytelling": """
            Frame the course content as an exciting story or journey. 
            Use narrative techniques, metaphors, and scenarios to explain concepts.
            Alex should be the main storyteller, while Nova asks clarifying questions and adds insights.
            Include a "What If" scenario that helps listeners imagine applying the knowledge.
        """,
        "debate": """
            Structure the podcast as a friendly debate between Alex and Nova.
            They should playfully disagree on approaches or interpretations of the course material.
            Use phrases like "On the other hand..." or "I see it differently..."
            End with both hosts finding common ground and summarizing key takeaways.
        """
    }
    
    # Get course details
    course_title = course_data["title"]
    course_description = course_data["description"]
    modules = course_data["modules"]
    
    # Select 1-2 modules to focus on
    focus_modules = modules[:2] if len(modules) > 1 else modules
    
    # Create prompt for OpenAI
    selected_style = styles.get(style, styles["storytelling"])
    
    prompt = f"""
Create a lively, engaging podcast script about the course: "{course_title}" convering the full concepts.
Don't say its a podcast, just write the script as if it's a conversation between two hosts.
No need mention the intros for hosts, just start with the conversation.

COURSE DESCRIPTION:
{course_description}

KEY MODULES TO COVER:
{', '.join([m['title'] for m in focus_modules])}

CONTENT DETAILS:
{focus_modules[0]['description'] if focus_modules and focus_modules[0]['description'] else ''}

PODCAST STYLE GUIDELINES:
{selected_style}

FORMAT REQUIREMENTS:
- Use two AI hosts named Alex and Nova
- Make the hosts' personalities vibrant and distinct
- Start with a catchy introduction
- Include a brief overview of what the course offers
- Cover key concepts from the selected modules
- End with a motivational conclusion that encourages listeners to take the course
- Format as a conversation with speaker names followed by colons:

Alex: ...
Nova: ...

IMPORTANT: Keep it light, engaging, and accessible to beginners. Explain concepts without using overly technical jargon.
"""
    
    # Generate the script
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1500
    )
    
    return response.choices[0].message.content

def synthesize_with_openai_tts(text: str, voice: str, output_path: str):
    """Convert text to speech using OpenAI's TTS API"""
    # Add a bit of SSML to make the voices more dynamic
    enhanced_text = text
    
    # Add extra animation for certain phrases (could be expanded)
    for phrase in ["Wow", "Amazing", "Incredible", "Oh my", "Really", "Wait"]:
        if phrase.lower() in text.lower():
            enhanced_text = text.replace(
                phrase, 
                f"{phrase}"
            )
    
    speech_response = client.audio.speech.create(
        model="tts-1-hd", # Use higher quality model
        voice=voice,
        input=enhanced_text,
        speed=1.0  # Normal speed, can be adjusted 0.8-1.2
    )
    
    with open(output_path, "wb") as f:
        f.write(speech_response.content)

def create_podcast_audio(script: str, output_dir: str = "podcast_audio"):
    """Convert podcast script to audio files"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean up any existing files
    for file in os.listdir(output_dir):
        if file.endswith(".mp3"):
            os.remove(os.path.join(output_dir, file))
    
    # Process each line of the script
    lines = script.strip().split('\n')
    audio_files = []
    
    for i, line in enumerate(lines):
        if ':' in line:
            try:
                speaker, text = line.split(':', 1)
                speaker = speaker.strip()
                text = text.strip()
                
                # Skip empty lines
                if not text:
                    continue
                
                # Assign voices - using more varied voices for interest
                if speaker.lower() == "alex":
                    # Randomly choose between male voices for Alex
                    voice = random.choice(["echo", "alloy", "fable"])
                elif speaker.lower() == "nova":
                    # Randomly choose between female voices for Nova
                    voice = random.choice(["nova", "shimmer"])
                else:
                    # Default fallback
                    voice = "alloy"
                
                # Create unique filename
                output_path = os.path.join(output_dir, f"{i:03d}_{speaker}.mp3")
                
                # Generate audio
                synthesize_with_openai_tts(text, voice, output_path)
                audio_files.append(output_path)
                
            except Exception as e:
                print(f"Error processing line {i}: {e}")
                continue
    
    return audio_files

from pydub import AudioSegment

def add_background_music(podcast_audio, background_music_path="media/background_music.mp3"):
    """Add background music to podcast at low volume"""
    try:
        # Make sure the background music file exists
        if not os.path.exists(background_music_path):
            print(f"Background music file not found: {background_music_path}")
            return podcast_audio
            
        # Load audio files
        podcast = AudioSegment.from_file(podcast_audio)
        background = AudioSegment.from_file(background_music_path)
        
        # Lower the volume of background music (adjust as needed)
        background = background - 15  # Reduce by 15 dB
        
        # Loop background if needed
        if len(background) < len(podcast):
            background = background * (len(podcast) // len(background) + 1)
            
        # Trim background to match podcast length
        background = background[:len(podcast)]
        
        # Mix podcast with background
        mixed = podcast.overlay(background)
        
        # Export the mixed audio
        mixed_output_path = podcast_audio.replace(".mp3", "_with_music.mp3")
        mixed.export(mixed_output_path, format="mp3")
        
        return mixed_output_path
    except Exception as e:
        print(f"Error adding background music: {e}")
        return podcast_audio

def merge_audio_files(files, output_file="podcast_episode.mp3"):
    """Merge multiple audio files into a single podcast"""
    if not files:
        return None
        
    # Sort files by filename to ensure correct order
    files.sort()
    
    # Create an empty audio segment
    combined = AudioSegment.empty()
    
    # Add a short silence between speakers
    silence = AudioSegment.silent(duration=300)  # 300ms
    
    # Add intro jingle
    try:
        intro_jingle = AudioSegment.from_file("media/intro_jingle.mp3")
        combined += intro_jingle
        combined += AudioSegment.silent(duration=500)  # 500ms silence after intro
    except:
        # No intro jingle available, continue without it
        pass
        
    # Combine all audio files
    for f in files:
        if os.path.exists(f):
            segment = AudioSegment.from_mp3(f)
            combined += segment
            combined += silence
    
    # Add outro jingle
    try:
        outro_jingle = AudioSegment.from_file("media/outro_jingle.mp3")
        combined += AudioSegment.silent(duration=500)  # 500ms silence before outro
        combined += outro_jingle
    except:
        # No outro jingle available, continue without it
        pass
    
    # Export the combined file
    combined.export(output_file, format="mp3")
    
    return output_file

def create_podcast(course_id: int, style="fun", output_file=None):
    """Create a podcast for a specific course"""
    # Get the course data
    course_data = get_course_content(course_id)
    
    if not course_data:
        print(f"Course with ID {course_id} not found")
        return None
    
    # Default output filename is based on course title
    if not output_file:
        # Sanitize course title for filename
        safe_title = "".join([c for c in course_data["title"] if c.isalnum() or c in " "])
        safe_title = safe_title.replace(" ", "_").lower()
        output_file = f"podcast_{safe_title}.mp3"
    
    # Generate the script
    print(f"Generating podcast script for course: {course_data['title']}")
    script = generate_podcast_script(course_data, style)
    
    # Save the script to a file
    script_file = output_file.replace(".mp3", "_script.txt")
    with open(script_file, "w") as f:
        f.write(script)
    
    # Create audio files for each line
    print("Converting script to audio...")
    output_dir = "podcast_audio_" + str(course_id)
    audio_files = create_podcast_audio(script, output_dir)
    
    # Merge audio files
    print("Merging audio files into podcast...")
    podcast_file = merge_audio_files(audio_files, output_file)
    
    # Add background music if available
    podcast_with_music = add_background_music(podcast_file)
    
    print(f"Podcast created successfully: {podcast_with_music or podcast_file}")
    return podcast_with_music or podcast_file