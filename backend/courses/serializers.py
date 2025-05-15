from rest_framework import serializers

from courses.models import CourseCategory, Course, Module, Lesson, User, UserCourseEnrollment, UserLessonProgress

class CourseCategorySerializer(serializers.ModelSerializer):
    courses_count = serializers.SerializerMethodField()

    def get_courses_count(self, obj):
        return Course.objects.filter(category=obj).count() if obj else 0
    class Meta:
        model = CourseCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
        }

class CourseListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    image = serializers.ImageField(source='thumbnail', allow_null=True, required=False)

    def get_category(self, obj):
        return obj.category.name if obj.category else None
    
    def get_duration(self, obj):
        lessons = Lesson.objects.filter(module__course=obj)
        total_duration = sum(lesson.estimated_duration for lesson in lessons if lesson.estimated_duration)
        return total_duration if lessons else 0
    
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

class ModuleSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        lessons = Lesson.objects.filter(module=obj)
        return lessons.count() if lessons else 0
    
    def get_duration(self, obj):
        lessons = Lesson.objects.filter(module=obj)
        total_duration = sum(lesson.estimated_duration for lesson in lessons if lesson.estimated_duration)
        return total_duration if lessons else 0
    
    def get_completed(self, obj):
        # TODO: General auth for many users
        user = User.objects.all().first()
        enrollment = UserCourseEnrollment.objects.filter(user=user, course=obj.course).first()
        user_progress = UserLessonProgress.objects.filter(enrollment=enrollment, lesson__module=obj).first()
        completed_lessons = UserLessonProgress.objects.filter(
            enrollment=enrollment,
            lesson__module=obj,
            status=UserLessonProgress.Status.COMPLETED
        ).count()
        total_lessons = Lesson.objects.filter(module=obj).count()
        if total_lessons == 0:
            return 0.0
        return (completed_lessons / total_lessons) * 100.0 if user_progress else 0.0

    class Meta:
        model = Module
        fields = ['id', 'title', 'lessons_count', 'duration', 'completed']
        read_only_fields = ['id']
        extra_kwargs = {
            'title': {'required': True},
        }
class CourseDetailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    lessons = serializers.SerializerMethodField()
    image = serializers.ImageField(source='thumbnail', allow_null=True, required=False)
    progress = serializers.SerializerMethodField()

    def get_lessons(self, obj):
        lessons = Lesson.objects.filter(module__course=obj)
        return lessons.count() if lessons else 0
    
    def get_progress(self, obj):
        # TODO: General auth for many users
        user = User.objects.all().first()  # Replace with actual user
        enrollment = UserCourseEnrollment.objects.filter(user=user, course=obj).first()
        if enrollment:
            return enrollment.progress_percentage
        return 0.0

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons', 'modules', 'image', 'progress']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'status': {'required': True},
        }