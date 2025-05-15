from django.contrib import admin
from courses.models import (
    CourseCategory,
    Course, 
    Module, 
    Lesson, 
    LessonContent, 
    Quiz,
    QuizQuestion,
    QuizAnswer,
    UserCourseEnrollment,
    UserLessonProgress
)
# Register your models here.

admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(LessonContent)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
admin.site.register(UserCourseEnrollment)
admin.site.register(UserLessonProgress)