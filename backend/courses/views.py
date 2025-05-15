import markdown2

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from courses.models import (
    CourseCategory,
    Course,
    Lesson,
    LessonContent
)
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
    def get(self, request, lesson_id):
        """
        Get course content
        """
        lesson = Lesson.objects.get(id=lesson_id)
        content = LessonContent.objects.get(lesson=lesson)
        if lesson.content_type == Lesson.ContentChoices.TEXT:
            response_content = markdown2.markdown(content.text_content)
        elif lesson.content_type == Lesson.ContentChoices.VIDEO:
            response_content = content.embed_code
        elif lesson.content_type == Lesson.ContentChoices.QUIZ:
            response_content = content.text_content
        else:
            response_content = None
        return Response({
            'lesson_id': lesson.id,
            'lesson_title': lesson.title,
            'content_type': lesson.content_type,
            'content': response_content
        })