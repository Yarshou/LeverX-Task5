from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions

import classroom.models
from classroom.models import Course, Solution


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
        homework_id = view.kwargs['homework_id']
        user_id = request.user.id
        solutions = Solution.objects.filter(homework_id=homework_id)
        try:
            get_object_or_404(solutions, user_id=user_id)
            return True
        except Http404:
            return False


class UserIsCourseMember(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'course_id' not in view.kwargs:
            return False
        else:
            course_id = view.kwargs['course_id']
        try:
            course = Course.objects.get(id=course_id)
        except classroom.models.Course.DoesNotExist:
            return False
        try:
            user_role = request.user.role
        except AttributeError:
            return False
        if user_role == 'Teacher':
            return course.teacher.filter(id=request.user.id).exists()
        elif user_role == 'Student':
            return course.student.filter(id=request.user.id).exists()
