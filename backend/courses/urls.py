from django.urls import path
from courses.views import (
    CourseCategoryListView,
    CourseListView
)

urlpatterns = [
    path('categories/', CourseCategoryListView.as_view(), name='course-categories'),
    path('courses/<int:category_id>/', CourseListView.as_view(), name='course-categories'),
]