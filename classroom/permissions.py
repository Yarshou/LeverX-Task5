from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from classroom.models import Course, Solution, Lecture


class SafeOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class UserIsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "Teacher"


class UserIsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "Student"


class StudentHasNoSolution(permissions.BasePermission):

    def has_permission(self, request, view):
        homework_id = view.kwargs['homework_id']
        user_id = request.user.id
        solutions = Solution.objects.filter(homework_id=homework_id)
        try:
            get_object_or_404(solutions, user_id=user_id)
            return False
        except Http404:
            return True


class UserSolutionOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        solution_id = view.kwargs['solution_id']
        user = request.user
        solution = Solution.objects.filter(id=solution_id)
        try:
            get_object_or_404(solution, user=user)
            return True
        except Http404:
            return False


class UserIsCourseMember(permissions.BasePermission):

    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_id', False)
        lecture_id = view.kwargs.get('lecture_id', False)
        homework_id = view.kwargs.get('homework_id', False)
        solution_id = view.kwargs.get('solution_id', False)

        try:
            course = Course.objects.get(
                Q(pk=course_id) |
                Q(related_lectures__id=lecture_id) |
                Q(related_lectures__related_homework__id=homework_id) |
                Q(related_lectures__related_homework__related_solution__id=solution_id)
            )
        except Course.MultipleObjectsReturned:
            return False
        except Course.DoesNotExist:
            return False

        try:
            user_role = request.user.role
        except AttributeError:
            return False
        if user_role == 'Teacher':
            return course.teacher.filter(id=request.user.id).exists()
        elif user_role == 'Student':
            return course.student.filter(id=request.user.id).exists()
