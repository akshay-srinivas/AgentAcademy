from django.db import models
from accounts.models import BaseModel, User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class CourseCategory(BaseModel):
    name = models.TextField()

    def __str__(self):
        return self.name



class Course(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
    title = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, related_name='courses')
    tags = models.JSONField(default=list, blank=True, help_text="List of tags for the course")
    description = models.TextField()
    status = models.TextField(
        choices=Status.choices,
        default=Status.DRAFT,
    )
    estimated_duration = models.PositiveIntegerField(help_text="Estimated duration in minutes")


    def __str__(self):
        return self.title
    

class Module(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.TextField()
    description = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return self.title
    

class Lesson(BaseModel):
    class ContentChoices(models.TextChoices):
        TEXT = 'text', 'Text'
        VIDEO = 'video', 'Video'
        QUIZ = 'quiz', 'Quiz'
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.TextField()
    content_type = models.TextField(
        choices=ContentChoices.choices,
        default=ContentChoices.TEXT,
    )
    is_mandatory = models.BooleanField(default=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('module', 'order')

    def __str__(self):
        return self.title
    

class LessonContent(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='content')
    
    text_content = models.TextField(blank=True)
    embed_code = models.TextField(blank=True, help_text="For video/interactive content")
    file_attachment = models.FileField(upload_to='lesson_files/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    
    # Additional metadata for specific content types
    content_metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"Content for {self.lesson.title}"
    

class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.TextField()
    description = models.TextField(blank=True)
    passing_score = models.PositiveIntegerField(default=70, validators=[
        MinValueValidator(1), MaxValueValidator(100)
    ])
    allowed_attempts = models.PositiveIntegerField(default=0, 
                                                help_text="0 means unlimited attempts")
    randomize_questions = models.BooleanField(default=False)
    show_correct_answers = models.BooleanField(default=True)
    time_limit_minutes = models.PositiveIntegerField(default=0, 
                                                  help_text="0 means no time limit")
    
    def __str__(self):
        return f"Quiz: {self.title}"


class QuizQuestion(models.Model):
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', 'Multiple Choice'
        TRUE_FALSE = 'true_false', 'True/False'
        SHORT_ANSWER = 'short_answer', 'Short Answer'
        MATCHING = 'matching', 'Matching'
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.TextField(choices=QuestionType.choices, default=QuestionType.MULTIPLE_CHOICE)
    explanation = models.TextField(blank=True, help_text="Explanation of the correct answer")
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    additional_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['quiz', 'order']
    
    def __str__(self):
        return f"Question {self.order}: {self.question_text}"


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"Answer: {self.answer_text}"
    

class UserCourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    last_accessed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
    @property
    def is_completed(self):
        return self.completed_at is not None
    
    def mark_completed(self):
        self.completed_at = timezone.now()
        self.progress_percentage = 100
        self.save(update_fields=['completed_at', 'progress_percentage'])

    
class UserLessonProgress(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
    enrollment = models.ForeignKey(UserCourseEnrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(null=True, blank=True)
    status = models.TextField(
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )
    
    class Meta:
        unique_together = ['enrollment', 'lesson']
    
    def __str__(self):
        return f"{self.enrollment.user.username} progress in {self.lesson.title}"
    
    def get_score(self):
        return self.score
    
    def mark_completed(self):
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

    def update_enrollment_progress(self):
        enrollment = self.enrollment
        course = enrollment.course

        mandatory_lessons_count = Lesson.objects.filter(
            module__course=course,
            is_mandatory=True,
            is_active=True
        ).count()

        if mandatory_lessons_count == 0:
            enrollment.progress_percentage = 100
        else:
            completed_mandatory_lessons_count = UserLessonProgress.objects.filter(
                enrollment=enrollment,
                lesson__is_mandatory=True,
                status=self.Status.COMPLETED
            ).count()
            enrollment.progress_percentage = (completed_mandatory_lessons_count / mandatory_lessons_count) * 100
        
        if enrollment.progress_percentage == 100 and not enrollment.is_completed:
            enrollment.mark_completed()
        else:
            enrollment.save(update_fields=['progress_percentage'])


# TODO: Implement a model for user quiz attempts
# TODO: Implement a model for user quiz results
# TODO: Implement a model for Learning Paths