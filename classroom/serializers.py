from rest_framework import serializers

from .models import User, Course, Lecture, Homework, Solution, Mark, Commentary


class CourseMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class CommentarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = CourseMemberSerializer(read_only=True)

    class Meta:
        model = Commentary
        fields = [
            'id',
            'user',
            'text',
        ]


class MarkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    commentaries = CommentarySerializer(source='related_commentary', many=True, read_only=True)

    class Meta:
        model = Mark
        fields = [
            'id',
            'value',
            'commentaries',
        ]


class SolutionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    mark = MarkSerializer(source='related_mark', many=False, read_only=True)

    class Meta:
        model = Solution
        fields = [
            'id',
            'solution',
            'mark',
        ]


class HomeworkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Homework
        fields = [
            'id',
            'title',
            'description',
            'deadline',
        ]


class HomeworkSolutionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    solutions = SolutionSerializer(source='related_solution', many=True, read_only=True)

    class Meta:
        model = Homework
        fields = [
            'id',
            'title',
            'description',
            'deadline',
            'solutions'
        ]


class LectureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    homeworks = HomeworkSerializer(source='related_homework', many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = [
            'id',
            'title',
            'description',
            'file',
            'homeworks',
        ]


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    lectures = LectureSerializer(source='related_lectures', many=True, read_only=True)

    teacher = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all().filter(role="Teacher"),
        required=False,
    )

    student = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all().filter(role="Student"),
        required=False,
    )

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'teacher',
            'student',
            'lectures',
        ]

    def create(self, validated_data):

        if 'teacher' in validated_data:
            teachers = validated_data.pop('teacher')
        else:
            teachers = list()
        if 'student' in validated_data:
            students = validated_data.pop('student')
        else:
            students = list()

        creator = validated_data.pop('creator')
        course = Course.objects.create(**validated_data)
        course.teacher.set(teachers)
        course.student.set(students)
        course.teacher.add(creator)
        return course
