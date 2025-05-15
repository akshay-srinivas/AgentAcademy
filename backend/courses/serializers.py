from rest_framework import serializers

from courses.models import CourseCategory, Course, Module, Lesson, User, UserCourseEnrollment

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
        }

class CourseSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    duration = serializers.IntegerField(source='estimated_duration', read_only=True)
    lessons = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    image = serializers.ImageField(source='thumbnail', allow_null=True, required=False)

    def get_category(self, obj):
        return obj.category.name if obj.category else None
    
    def get_lessons(self, obj):
        lessons = Lesson.objects.filter(module__course=obj)
        return lessons.count() if lessons else 0
    
    def get_completed(self, obj):
        # TODO: General auth for many users
        user = User.objects.all().first()  # Replace with actual user
        enrollment = UserCourseEnrollment.objects.filter(user=user, course=obj).first()
        if enrollment:
            return enrollment.progress_percentage
        return 0.0

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons', 'duration', 'category', 'completed', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'status': {'required': True},
        }