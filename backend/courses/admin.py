from agentacademy.admin import admin_site
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

admin_site.register(CourseCategory)
admin_site.register(Course)
admin_site.register(Module)
admin_site.register(Lesson)
admin_site.register(LessonContent)
admin_site.register(Quiz)
admin_site.register(QuizQuestion)
admin_site.register(QuizAnswer)
admin_site.register(UserCourseEnrollment)
admin_site.register(UserLessonProgress)