from django.core.management.base import BaseCommand

from courses.models import Course, Module, Lesson, LessonContent
from courses.constants import COURSES, MODULES, LESSONS, LESSON_CONTENT


class Command(BaseCommand):
    help = "Setup initial data for the application"

    def setup_courses(self):
        for course_data in COURSES:
            course, created = Course.objects.get_or_create(
                title=course_data["title"],
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created course: {course.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Course already exists: {course.title}"))

    def setup_modules(self):
        for module_data in MODULES:
            course = Course.objects.get(title=module_data["course_title"])
            for order, module in enumerate(module_data["modules"], 1):
                module_obj, created = Module.objects.get_or_create(
                    course=course,
                    title=module["title"],
                    order=order,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created module: {module_obj.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Module already exists: {module_obj.title}"))

    def setup_lessons(self):
        for lesson_data in LESSONS:
            module = Module.objects.get(title=lesson_data["module_title"])
            for order, lesson in enumerate(lesson_data["lessons"], 1):
                lesson_obj, created = Lesson.objects.get_or_create(
                    module=module,
                    title=lesson["title"],
                    content_type=lesson["content_type"],
                    estimated_duration=lesson["estimated_duration"],
                    is_mandatory=lesson["is_mandatory"],
                    order=order,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created lesson: {lesson_obj.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Lesson already exists: {lesson_obj.title}"))

    def setup_lesson_content(self):
        for lesson_content_data in LESSON_CONTENT:
            lesson = Lesson.objects.get(title=lesson_content_data["lesson_title"])
            if lesson_content_data.get("text_content"):
                content_obj, created = LessonContent.objects.get_or_create(
                    lesson=lesson,
                    text_content=lesson_content_data["text_content"],
                )
            elif lesson_content_data.get("embed_code"):
                content_obj, created = LessonContent.objects.get_or_create(
                    lesson=lesson,
                    embed_code=lesson_content_data["embed_code"],
                )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created content for lesson: {content_obj.lesson.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Content already exists for lesson: {content_obj.lesson.title}"))

    def handle(self, *args, **kwargs):
        self.stdout.write("Setting up initial data...")
        self.setup_courses()
        self.setup_modules()
        self.setup_lessons()
        self.setup_lesson_content()
        self.stdout.write(self.style.SUCCESS("Initial data setup complete."))
