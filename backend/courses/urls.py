from django.urls import path
from courses.views import (
    CourseCategoryListView,
    CourseListView,
    CourseDetailView,
    LessonContentView,
)

urlpatterns = [
    path('categories/', CourseCategoryListView.as_view(), name='course-categories'),
    path('courses/<int:category_id>/', CourseListView.as_view(), name='course-categories'),
    path('course/<str:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/<str:course_id>/lesson/<int:lesson_id>/', LessonContentView.as_view(), name='lesson-content'),
]