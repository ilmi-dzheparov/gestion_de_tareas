from django.db import models
from django.conf import settings # Best practice: refer to the User model via settings
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name='titulo')
    description = models.TextField(null=False, blank=True, verbose_name='descripcion')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='fecha de terminacion')
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tasks_as_student',
        limit_choices_to={'is_student': True},
        verbose_name='alumnos'
    )
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='tasks_as_tutor',
        limit_choices_to={'is_tutor': True},
        verbose_name='tutor')
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        # limit_choices_to={'archived': False},
        related_name='tasks',
        verbose_name='cursos')

    def __str__(self):
        return f"{self.title}"


class Stage(models.Model):
    count = models.PositiveIntegerField(verbose_name='orden')
    title = models.CharField(max_length=100, verbose_name='titulo')
    description = models.TextField(null=False, blank=True, verbose_name='descripcion')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='fecha de inicio')
    end_date = models.DateTimeField(verbose_name='fecha de terminacion')
    status = models.BooleanField()
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        # limit_choices_to={'archived': False},
        related_name='stages',
        verbose_name='tarea')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='stages',
        limit_choices_to={'is_student': True},
        verbose_name='alumno')

    class Meta:
        # Ensures stages appear in order (1, 2, 3...) in the admin and queries
        ordering = ['count']

    def __str__(self):
        return f"{self.title} - Task: {self.task}"

    @property
    def is_overdue(self):
        return not self.status and self.end_date < timezone.now()

    # class Student(models.Model):
    #     dni = models.CharField(max_length=10)
    #     name = models.CharField(max_length=100)
    #     last_name_1 = models.CharField(max_length=100)
    #     last_name_2 = models.CharField(max_length=100)
    #     email = models.EmailField()
    #     birthdate = models.DateField()
    #     department = models.ForeignKey(Department,
    #                                    on_delete=models.PROTECT,
    #                                    related_name='students')
    #
    #
    #     def __str__(self):
    #         return f"{self.last_name_1} {self.last_name_2}, {self.name}"

    # class Tutor(models.Model):
    #     name = models.CharField(max_length=100)
    #     last_name_1 = models.CharField(max_length=100)
    #     last_name_2 = models.CharField(max_length=100)
    #     email = models.EmailField(null=True, blank=True)
    #
    #     def __str__(self):
    #         return f"{self.last_name_1} {self.last_name_2}, {self.name}"

