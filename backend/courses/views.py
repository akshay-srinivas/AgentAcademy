import markdown2

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from courses.models import (
    CourseCategory,
    Course,
    Lesson,
    LessonContent,
    UserLessonProgress,
    UserCourseEnrollment
)
from accounts.models import User
from courses.serializers import (
    CourseCategorySerializer,
    CourseListSerializer,
    CourseDetailSerializer
)

# TODO: Implement Views for the following:
# 1. List Modules
# 2. Get Lesson for Module
# 3. Get Lesson Content
# 4. Get User Course Progress
# 5. Get User Module Progress


class CourseCategoryListView(APIView):
    def get(self, request):
        """
        List all course categories
        """
        categories = CourseCategorySerializer(CourseCategory.objects.all(), many=True).data
        return Response(categories)


class CourseListView(APIView):
    def get(self, request, category_id):
        """
        List all courses in a category
        """
        courses = CourseListSerializer(Course.objects.filter(category_id=category_id), many=True).data
        return Response(courses)
    

class CourseDetailView(APIView):
    def get(self, request, course_id):
        """
        Get course details
        """
        course = CourseDetailSerializer(Course.objects.get(id=course_id)).data
        return Response(course)


class LessonContentView(APIView):
    def get(self, request, course_id, lesson_id):
        """
        Get course content
        """
        course = Course.objects.get(id=course_id)
        lessons = Lesson.objects.filter(module__course=course).order_by('module__order')
        if lessons.exists():
            if len(lessons) < lesson_id:
                return Response({'error': 'Lesson not found'}, status=404)
            lesson = lessons[lesson_id - 1]
        content = LessonContent.objects.get(lesson=lesson)
        if lesson.content_type == Lesson.ContentChoices.TEXT:
            response_content = markdown2.markdown(content.text_content)
        elif lesson.content_type == Lesson.ContentChoices.VIDEO:
            response_content = content.embed_code
        elif lesson.content_type == Lesson.ContentChoices.QUIZ:
            response_content = content.text_content
        else:
            response_content = None
        completed = False
        # Sample User
        user = User.objects.all().first()
        user_course_enrollment = UserCourseEnrollment.objects.filter(user=user, course=course).first()
        user_lesson_progress = UserLessonProgress.objects.filter(
            enrollment__user=user,
            lesson=lesson
        ).first()
        if user_lesson_progress:
            completed = user_lesson_progress.status == UserLessonProgress.Status.COMPLETED
        

        return Response({
            'lesson_id': lesson.id,
            'lesson_title': lesson.title,
            'content_type': lesson.content_type,
            'content': response_content,
            'completed': completed,
        })
    
    def post(self, request, course_id, lesson_id):
        """
        Mark a lesson as complete
        """
        course = Course.objects.get(id=course_id)
        lessons = Lesson.objects.filter(module__course=course).order_by('module__order')
        if lessons.exists():
            if len(lessons) < lesson_id:
                return Response({'error': 'Lesson not found'}, status=404)
            lesson = lessons[lesson_id - 1]
        # Sample User
        user = User.objects.all().first()# Replace with actual user from request
        user_course_enrollment, created = UserCourseEnrollment.objects.get_or_create(
            user=user,
            course=course
        )
            
        user_lesson_progress, created = UserLessonProgress.objects.get_or_create(
            enrollment=user_course_enrollment,
            lesson=lesson
        )
        if created:
            user_lesson_progress.mark_completed()
            user_lesson_progress.update_enrollment_progress()
        else:
            return Response({'message': 'Lesson already marked as complete'})
        return Response({'message': 'Lesson marked as complete'})   
