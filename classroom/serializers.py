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

    def create(self, validated_data):
        user = validated_data.pop('user')
        mark_id = validated_data.pop('mark_id')
        mark = Mark.objects.get(id=mark_id)
        return Commentary.objects.create(user=user, mark=mark, **validated_data)


class MarkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    commentaries = CommentarySerializer(source='commentary', many=True, read_only=True)

    class Meta:
        model = Mark
        fields = [
            'id',
            'value',
            'commentaries',
        ]

    def create(self, validated_data):
        creator = validated_data.pop('creator')
        solution_id = validated_data.pop('solution_id')
        solution = Solution.objects.get(id=solution_id)
        value = validated_data.pop('value')
        try:
            mark = Mark.objects.get(solution=solution)
            mark.user_id = creator
            mark.value = value
            mark.save()
            return mark
        except Mark.DoesNotExist:
            return Mark.objects.create(user=creator, solution=solution, value=value)


class SolutionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    mark = MarkSerializer(source='marks', many=False, read_only=True)

    class Meta:
        model = Solution
        fields = [
            'id',
            'solution',
            'mark',
        ]

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        homework_id = validated_data.pop('homework_id')
        homework = Homework.objects.get(id=homework_id)
        return Solution.objects.create(user=user_id, homework=homework, **validated_data)


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

    def create(self, validated_data):
        lecture_id = validated_data.pop('lecture_id')
        lecture = Lecture.objects.get(id=lecture_id)
        return Homework.objects.create(lecture=lecture, **validated_data)


class HomeworkSolutionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    solutions = SolutionSerializer(source='solution', many=True, read_only=True)

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
    homeworks = HomeworkSerializer(source='homework', many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = [
            'id',
            'title',
            'description',
            'file',
            'homeworks',
        ]

    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        course = Course.objects.get(id=course_id)
        return Lecture.objects.create(course=course, **validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    lectures = LectureSerializer(source='lecture', many=True, read_only=True)

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
