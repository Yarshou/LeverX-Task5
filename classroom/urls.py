from django.urls import path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register("course", views.CourseListDetailView, basename='course-detail')

urlpatterns = [
    path(
        'course-add-member/<int:course_id>/',
        views.CourseListAddMemberView.as_view()
    ),
    path(
        'course-delete-member/<int:course_id>/',
        views.CourseListDeleteMemberView.as_view()
    ),
    path(
        'course/<int:course_id>/lecture-create/',
        views.LectureListCreateView.as_view()
    ),
    path(
        'course/<int:course_id>/lecture/<int:lecture_id>/',
        views.LectureListDetailView.as_view()
    ),
    path(
        'course/<int:course_id>/lecture/<int:lecture_id>/homework-create/',
        views.HomeworkListCreateView.as_view()
    ),
    path(
        'course/<int:course_id>/lecture/<int:lecture_id>/homework/<int:homework_id>/',
        views.HomeworkListDetailView.as_view()
    ),
    path(
        'course/<int:course_id>/homework-solutions/<int:homework_id>',
        views.HomeworkSolutionsDetailView.as_view()
    ),
    path(
        'course/<int:course_id>/homework/<int:homework_id>/solution-add/',
        views.SolutionListCreateView.as_view()
    ),
    path(
        'course/<int:course_id>/homework/<int:homework_id>/solution/<int:solution_id>/',
        views.SolutionDetailView.as_view()
    ),
    path(
        'course/<int:course_id>/solution/<int:solution_id>/mark-add/',
        views.MarkCreateView.as_view()
    ),
    path(
        'course/<int:course_id>/solution/<int:solution_id>/mark/<int:mark_id>/',
        views.MarkDetailView.as_view()
    ),
    path(
        'course/<int:course_id>/mark/<int:mark_id>/commentary/',
        views.CommentaryCreateView.as_view()
    ),

]

urlpatterns += router.urls
