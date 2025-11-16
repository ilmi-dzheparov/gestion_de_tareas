from django.core.management import BaseCommand
from taskapp.models import Student, Department

class Command(BaseCommand):
    """Create Students"""
    def handle(self, *args, **options)
        self.stdout.write("Create department and students")
        department_name = "ASIX"
        student_names = [
            ["z0073269z", "Ilmi", "Dzhep", "", "ilmi@gmail.com", "1981-03-29 12:00"],
            ["z0073270z", "Carlos", "Pedro", "Ramirez", "carlos@gmail.com", "1982-03-29 12:00"],
        ]
        department, created= Department.objects.get_or_create(name=department_name)
        self.stdout.write(f"Department created {department.name}")
        for name in student_names:
            student, created = Student.objects.get_or_create(
                dni=name[0],
                name=name[1],
                last_name_1=name[2],
                last_name_2=name[3],
                email=name[4],
                birthdate=name[5],
            )
            self.stdout.write(f"Student created {student.name}")


