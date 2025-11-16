from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

class Student(models.Model):
    dni = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    last_name_1 = models.CharField(max_length=100)
    last_name_2 = models.CharField(max_length=100)
    email = models.EmailField()
    birthdate = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

class Tutor(models.Model):
    name = models.CharField(max_length=100)
    last_name_1 = models.CharField(max_length=100)
    last_name_2 = models.CharField(max_length=100)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    students = models.ManyToManyField(Student, related_name='tasks')
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT)
