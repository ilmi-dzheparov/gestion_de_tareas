import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from taskapp.models import Task, Course
from django.utils.dateparse import parse_datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт задач из CSV файла'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **options):
        file_path = options['csv_file']

        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0

                for row in reader:
                    # 1. Ищем курс по названию (или ID)
                    course_name = row.get('course')
                    course = Course.objects.filter(name=course_name).first()
                    if not course:
                        self.stdout.write(self.style.WARNING(f"Курс '{course_name}' не найден. Пропуск строки."))
                        continue

                    # 2. Ищем тьютора по email
                    tutor_email = row.get('tutor_email')
                    tutor = User.objects.filter(email=tutor_email, is_tutor=True).first()
                    if not tutor:
                        self.stdout.write(self.style.WARNING(f"Тьютор '{tutor_email}' не найден. Пропуск."))
                        continue

                    # 3. Создаем задачу
                    task, created = Task.objects.update_or_create(
                        title=row['title'],
                        course=course,
                        defaults={
                            'description': row.get('description', ''),
                            'end_date': parse_datetime(row.get('end_date')),
                            'tutor': tutor,
                        }
                    )

                    # 4. Добавляем студентов (ManyToManyField)
                    # Ожидаем email-ы студентов через запятую: "s1@mail.com,s2@mail.com"
                    student_emails = row.get('student_emails', '').split(',')
                    if student_emails:
                        students = User.objects.filter(email__in=[e.strip() for e in student_emails], is_student=True)
                        task.students.set(students)

                    action = "Создана" if created else "Обновлена"
                    self.stdout.write(self.style.SUCCESS(f"{action} задача: {task.title}"))
                    count += 1

                self.stdout.write(self.style.SUCCESS(f"Импорт завершен. Всего: {count}"))

        except FileNotFoundError:
            raise CommandError(f"Файл {file_path} не найден")