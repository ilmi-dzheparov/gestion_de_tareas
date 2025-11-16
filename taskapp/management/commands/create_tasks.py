from django.core.management import BaseCommand
from taskapp.models import Task, Department


class Command(BaseCommand):
    """Create tasks"""
    def handle(self, *args, **options):
        self.stdout.write("Create tasks")
        task_names = [
            "Task-1",
            "Task_2",
            "Task_3",
        ]
        # task = Task.objects.get_or_create
        for task_name in task_names:
            task, created = Task.objects.get_or_create(title=task_name)
            self.stdout.write(f"Created task {task.title}")
        self.stdout.write(self.style.SUCCESS("Tasks created"))
