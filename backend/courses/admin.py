from agentacademy.admin import admin_site
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
from courses.podcast import create_podcast
from django.contrib import messages
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']  # Adjust fields as needed
    # list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'status']
    actions = ["create_podcast"]

    @admin.action(description="Create a Podcast")
    def create_podcast(modeladmin, request, queryset):
        # Logic to create a podcast
        for course in queryset:
            try:
                # Assuming you have a method to generate the podcast script
                create_podcast(course_id=course.id)
                messages.success(request, f"Podcast created for {course.title}")
            except Exception as e:
                messages.error(request, f"Error creating podcast for {course.title}: {str(e)}")
    

admin_site.register(CourseCategory)
admin_site.register(Course, CourseAdmin)
admin_site.register(Module)
admin_site.register(Lesson)
admin_site.register(LessonContent)
admin_site.register(Quiz)
admin_site.register(QuizQuestion)
admin_site.register(QuizAnswer)
admin_site.register(UserCourseEnrollment)
admin_site.register(UserLessonProgress)