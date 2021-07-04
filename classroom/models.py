from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICE_FIELDS = (
        ("Student", "Student"),
        ("Teacher", "Teacher")
    )

    role = models.CharField(choices=CHOICE_FIELDS, max_length=10)

    REQUIRED_FIELDS = [
        'email',
        'role'
    ]


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    teacher = models.ManyToManyField(User, related_name='teacher')
    student = models.ManyToManyField(User, related_name='student')

    class Meta:
        ordering = ['create_date']

    def __str__(self):
        return str(self.title)

    @property
    def lectures(self):
        return self.related_lectures.all()


class Lecture(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="path", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='related_lectures')

    class Meta:
        ordering = ['create_date']

    def __str__(self):
        return str(self.title)

    @property
    def homework(self):
        return self.related_homework.all()


class Homework(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='related_homework')

    class Meta:
        ordering = ['create_date']

    def __str__(self):
        return str(self.title)

    @property
    def solution(self):
        return self.related_solution.all()


class Solution(models.Model):
    solution = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='related_solution')

    @property
    def mark(self):
        return self.related_mark


class Mark(models.Model):
    value = models.SmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.OneToOneField(Solution, on_delete=models.CASCADE, related_name='related_mark')

    @property
    def commentary(self):
        return self.related_commentary.all()


class Commentary(models.Model):
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentary_user')
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='related_commentary')

    class Meta:
        ordering = ['create_date']
