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
    birthdate = models.DateField()
    department = models.ForeignKey(Department,
                                   on_delete=models.PROTECT,
                                   related_name='students')


    def __str__(self):
        return f"{self.last_name_1} {self.last_name_2}, {self.name}"

class Tutor(models.Model):
    name = models.CharField(max_length=100)
    last_name_1 = models.CharField(max_length=100)
    last_name_2 = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name_1} {self.last_name_2}, {self.name}"

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    students = models.ManyToManyField(Student, related_name='tasks')
    tutor = models.ForeignKey(Tutor,
                              on_delete=models.PROTECT,
                              related_name='tasks',
                              verbose_name='tutor')
    course = models.ForeignKey(Course,
                              on_delete=models.PROTECT,
                              related_name='tasks',
                              verbose_name='course')


class Stage(models.Model):
    count = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.BooleanField()
    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE,
                             limit_choices_to={'archived': False},
                             related_name='stages',
                             verbose_name='etapa')

