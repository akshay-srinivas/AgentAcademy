from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from courses.models import (
    CourseCategory,
    Course
)
from courses.serializers import (
    CourseCategorySerializer,
    CourseSerializer
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
        courses = CourseSerializer(Course.objects.filter(category_id=category_id), many=True).data
        return Response(courses)