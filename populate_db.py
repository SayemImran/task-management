# import os
# import django
# from faker import Faker
# import random
# from tasks.models import Employee, Project, Tasks, TaskDetail

# # Set up Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
# django.setup()

# # Function to populate the database


# def populate_db():
#     # Initialize Faker
#     fake = Faker()

#     # Create Projects
#     projects = [Project.objects.create(
#         name=fake.bs().capitalize(),
#         description=fake.paragraph(),
#         start_date=fake.date_this_year()
#     ) for _ in range(5)]
#     print(f"Created {len(projects)} projects.")

#     # Create Employees
#     employees = [Employee.objects.create(
#         name=fake.name(),
#         email=fake.email()
#     ) for _ in range(10)]
#     print(f"Created {len(employees)} employees.")

#     # Create Tasks
#     tasks = []
#     for _ in range(20):
#         task = Tasks.objects.create(
#             project=random.choice(projects),
#             title=fake.sentence(),
#             description=fake.paragraph(),
#             due_date=fake.date_this_year(),
#             status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
#             is_completed=random.choice([True, False])
#         )
#         task.assigned_to.set(random.sample(employees, random.randint(1, 3)))
#         tasks.append(task)
#     print(f"Created {len(tasks)} tasks.")

#     # Create Task Details 
#     for task in tasks:
#         TaskDetail.objects.create(
#             task=task,
#             assigned_to=", ".join(
#                 [emp.name for emp in task.assigned_to.all()]),
#             priority=random.choice(['H', 'M', 'L']),
#             notes=fake.paragraph()
#         )
#     print("Populated TaskDetails for all tasks.")
#     print("Database populated successfully!")





import os
import django
import sys

# ----- 1. Set project path -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# ----- 2. Setup Django settings module BEFORE importing models -----
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

# ----- 3. Now import your models -----
from tasks.models import Employee, Project, Tasks, TaskDetail

from faker import Faker
import random

def populate_db():
    fake = Faker()

    projects = [
        Project.objects.create(
            name=fake.bs().capitalize(),
            description=fake.paragraph(),
            start_date=fake.date_this_year()
        )
        for _ in range(5)
    ]

    employees = [
        Employee.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        for _ in range(10)
    ]

    tasks = []
    for _ in range(20):
        task = Tasks.objects.create(
            project=random.choice(projects),
            title=fake.sentence(),
            description=fake.paragraph(),
            due_date=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            is_completed=random.choice([True, False])
        )
        task.assigned_to.set(random.sample(employees, random.randint(1, 3)))
        tasks.append(task)

    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            assigned_to=", ".join(emp.name for emp in task.assigned_to.all()),
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
