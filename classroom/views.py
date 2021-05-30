from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from .models import Course, User, Lecture, Homework, Solution, Mark

from .permissions import UserIsTeacher, UserIsStudent, SafeOnly, UserIsCourseMember, StudentHasNoSolution, \
    UserSolutionOwner
from .serializers import CourseSerializer, CourseMemberSerializer, LectureSerializer, HomeworkSerializer, \
    SolutionSerializer, HomeworkSolutionsSerializer, MarkSerializer, CommentarySerializer


class CourseListDetailView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticated,
        UserIsTeacher | SafeOnly,
    ]
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CourseListAddMemberView(generics.ListCreateAPIView):
    serializer_class = CourseMemberSerializer
    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher,
    ]

    def post(self, request, *args, **kwargs):
        member = request.data.get('username')
        course = get_object_or_404(Course, id=kwargs['course_id'])
        user = get_object_or_404(User, username=member)
        if user.role == 'Student':
            course.student.add(user)
        elif user.role == 'Teacher':
            course.teacher.add(user)
        else:
            return Response(data=None, status=HTTP_400_BAD_REQUEST)

        return Response(data=CourseSerializer(course).data, status=HTTP_200_OK)


class CourseListDeleteMemberView(generics.DestroyAPIView):
    serializer_class = CourseMemberSerializer
    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher,
    ]

    def delete(self, request, *args, **kwargs):
        member = request.data.get('username')
        course = get_object_or_404(Course, id=kwargs['course_id'])
        user = get_object_or_404(User, username=member)
        if user.role == 'Student':
            course.student.remove(user)
        elif user.role == 'Teacher':
            return Response(data={'payload': 'You can\'t delete Teacher'}, status=HTTP_403_FORBIDDEN)
        else:
            return Response(data={'payload': 'Incorrect data'}, status=HTTP_400_BAD_REQUEST)
        return Response(data=CourseSerializer(course).data, status=HTTP_200_OK)


class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureSerializer

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher,
    ]

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'])


class LectureListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    lookup_url_kwarg = 'lecture_id'

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher | SafeOnly,
    ]

    def get(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        lecture_id = kwargs['lecture_id']
        course = Course.objects.get(id=course_id)
        lectures = Lecture.objects.filter(course=course)
        lecture = get_object_or_404(lectures, id=lecture_id)
        return Response(LectureSerializer(lecture).data, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        lecture_id = kwargs['lecture_id']
        course = Course.objects.get(id=course_id)
        lectures = Lecture.objects.filter(course=course)
        lecture = get_object_or_404(lectures, id=lecture_id)
        return Response(LectureSerializer(lecture).data, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        lecture_id = kwargs['lecture_id']
        course = Course.objects.get(id=course_id)
        lectures = Lecture.objects.filter(course=course)
        lecture = get_object_or_404(lectures, id=lecture_id)
        lecture.delete()
        return Response(LectureSerializer(lecture).data, status=HTTP_200_OK)


class HomeworkListCreateView(generics.ListCreateAPIView):
    serializer_class = HomeworkSerializer

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher
    ]

    def perform_create(self, serializer):
        serializer.save(lecture_id=self.kwargs['lecture_id'])


class HomeworkListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()
    lookup_url_kwarg = 'homework_id'

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher | SafeOnly
    ]


class HomeworkSolutionsDetailView(generics.RetrieveAPIView):
    serializer_class = HomeworkSolutionsSerializer
    queryset = Homework.objects.all()
    lookup_url_kwarg = 'homework_id'

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher,
    ]


class SolutionListCreateView(generics.ListCreateAPIView):
    serializer_class = SolutionSerializer
    permission_classes = [
        IsAuthenticated,
        UserIsStudent,
        UserIsCourseMember,
        StudentHasNoSolution,
    ]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user, homework_id=self.kwargs['homework_id'])


class SolutionDetailView(generics.RetrieveAPIView):
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()
    lookup_url_kwarg = 'solution_id'

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        (UserIsStudent and UserSolutionOwner) |
        UserIsTeacher,
    ]


class MarkCreateView(generics.ListCreateAPIView):
    serializer_class = MarkSerializer

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        UserIsTeacher,
    ]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, solution_id=self.kwargs['solution_id'])


class MarkDetailView(generics.RetrieveAPIView):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()
    lookup_url_kwarg = 'mark_id'

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        (UserIsStudent and UserSolutionOwner) |
        UserIsTeacher
    ]

    def get(self, request, *args, **kwargs):
        solution_id = kwargs['solution_id']
        mark_id = kwargs['mark_id']
        mark = Mark.objects.filter(solution_id=solution_id)
        marks = get_object_or_404(mark, id=mark_id)
        return Response(MarkSerializer(marks).data, status=HTTP_200_OK)


class CommentaryCreateView(generics.ListCreateAPIView):
    serializer_class = CommentarySerializer

    permission_classes = [
        IsAuthenticated,
        UserIsCourseMember,
        (UserIsStudent and UserSolutionOwner) |
        UserIsTeacher
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, mark_id=self.kwargs['mark_id'])
