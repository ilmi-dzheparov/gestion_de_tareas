import os

from django.db import models
from django.conf import settings # Best practice: refer to the User model via settings
from django.utils import timezone


class Department(models.Model):
    """
    Representa las áreas académicas (ej. Matemáticas, Ciencias, Idiomas).
    Sirve como nivel superior de organización en el centro educativo.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Departamento")
    name_short = models.CharField(max_length=100, unique=True, verbose_name="Siglas")
    def __str__(self):
        return f"{self.name_short}"

class Group(models.Model):
    """
    Define las cohortes o grupos de alumnos según su departamento y año académico.
    Permite segmentar a los alumnos para asignar tareas masivas por grupo.
    """
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="Departamento")
    year = models.PositiveIntegerField(verbose_name="Año Académico")
    def __str__(self):
        return f"{self.department}-{self.year}"

class Course(models.Model):
    """
    Asignaturas específicas vinculadas a un departamento.
    Es el nexo de unión con el modelo Task (Tarea).
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Curso")
    name_short = models.CharField(max_length=100, unique=True, verbose_name="Código/Siglas")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="Departamento")

    def __str__(self):
        return f"{self.name_short}.{self.name}"

class Task(models.Model):
    """
    Modelo principal para la gestión de tareas académicas.
    Relaciona a tutores, alumnos y cursos en una sola entidad.
    """

    # Identificador visual de la tarea
    title = models.CharField(max_length=100, verbose_name='titulo')
    # Descripción detallada de la actividad (obligatoria en DB, opcional en formulario)
    description = models.TextField(null=False, blank=True, verbose_name='descripcion')
    # Fecha de creación generada automáticamente al guardar la tarea
    start_date = models.DateTimeField(auto_now_add=True)
    # Fecha límite establecida por el tutor para la entregaS
    end_date = models.DateTimeField(verbose_name='fecha de terminacion')
    # Relación Muchos-a-Muchos: Permite asignar una tarea a varios alumnos a la vez.
    # El filtro 'is_student' asegura que solo se listen usuarios con rol de alumno.
    # Representa si la etapa ha sido completada (True) o sigue pendiente (False)
    status = models.BooleanField(default=False, verbose_name='completada')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Autor de la tarea',
        null=True,
        blank=True
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tasks_as_student',
        limit_choices_to={'is_student': True},
        verbose_name='alumnos'
    )
    # Relación Uno-a-Muchos: Define al profesor responsable.
    # PROTECT evita borrar el tutor si tiene tareas activas asignadas.
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='tasks_as_tutor',
        limit_choices_to={'is_tutor': True},
        verbose_name='tutor')
    # Relación Uno-a-Muchos: Vincula la tarea a una asignatura o curso específico.
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        # limit_choices_to={'archived': False},
        related_name='tasks',
        verbose_name='cursos')

    @property
    def days_left(self):
        if self.end_date:
            delta = self.end_date - timezone.now()
            return delta.days
        return None

    def __str__(self):
        """Retorna el título para identificar la tarea en el panel de admin y selects"""
        return f"{self.title}"

class TaskFile(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='tarea'
    )
    file = models.FileField(
        upload_to='tasks/attachments/%Y/%m/%d/',
        verbose_name='archivo'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archivo para {self.task.title}"

    def filename(self):
        return os.path.basename(self.file.name)

class Stage(models.Model):
    """
    Representa las etapas o hitos individuales de una tarea.
    Permite el seguimiento granular del progreso de cada alumno.
    """

    # Orden secuencial de la etapa (se autocalcula en el método save)
    count = models.PositiveIntegerField(verbose_name='orden')
    title = models.CharField(max_length=100, verbose_name='titulo')
    description = models.TextField(null=False, blank=True, verbose_name='descripcion')
    # Fechas de control para medir el tiempo de ejecución por etapa
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='fecha de inicio')
    end_date = models.DateTimeField(verbose_name='fecha de terminacion')
    # Representa si la etapa ha sido completada (True) o sigue pendiente (False)
    status = models.BooleanField(default=False, verbose_name='completada')
    # Relación con la Tarea: Si se borra la tarea, se borran sus etapas (CASCADE)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        # limit_choices_to={'archived': False},
        related_name='stages',
        verbose_name='tarea')
    # Relación con el Alumno: Seguimiento individualizado de la etapa
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='stages',
        limit_choices_to={'is_student': True},
        verbose_name='alumno')
    class Meta:
        # Ensures stages appear in order (1, 2, 3...) in the admin and queries
        ordering = ['task', 'count']
    def __str__(self):
        return f"{self.title} - Task: {self.task}"

    def save(self, *args, **kwargs):
        """
        Lógica funcional: Autocalcula el número de etapa.
        Si es la primera etapa de la tarea será 1, si no, incrementa el último valor.
        """
        if not self.pk:  # Solo se ejecuta al crear una nueva etapa
            last_stage = Stage.objects.filter(task=self.task).order_by('-count').first()
            if last_stage:
                self.count = last_stage.count + 1
            else:
                self.count = 1
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """
        Función de utilidad: Verifica si la etapa está fuera de plazo.
        Retorna True si no está completada y la fecha actual superó la de terminación.
        """
        return not self.status and self.end_date < timezone.now()

    @property
    def days_left(self):
        if self.end_date:
            delta = self.end_date - timezone.now()
            return delta.days
        return None

    def __str__(self):
        """Retorna el título para identificar la tarea en el panel de admin y selects"""
        return f"{self.title}"

class StageFile(models.Model):
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='etapa'
    )
    file = models.FileField(
        upload_to='stages/attachments/%Y/%m/%d/',
        verbose_name='archivo'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archivo para {self.stage.title}"

    def filename(self):
        return os.path.basename(self.file.name)
