from django.core.management.base import BaseCommand

from courses.models import Course, Module, Lesson, LessonContent, Quiz, QuizQuestion, QuizAnswer

class Command(BaseCommand):
    help = "Clear all data from the database"

    def handle(self, *args, **kwargs):
        # Clear all data from the database
        Course.objects.all().delete()
        Module.objects.all().delete()
        Lesson.objects.all().delete()
        LessonContent.objects.all().delete()
        Quiz.objects.all().delete()
        QuizQuestion.objects.all().delete()
        QuizAnswer.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All data cleared successfully."))