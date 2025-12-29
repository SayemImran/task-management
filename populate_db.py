# import os
# import django
# import sys

# # ----- 1. Set project path -----
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)

# # ----- 2. Setup Django settings module BEFORE importing models -----
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
# django.setup()

# # ----- 3. Now import your models -----
# from tasks.models import Employee, Project, Tasks, TaskDetail

# from faker import Faker
# import random

# def populate_db():
#     fake = Faker()

#     projects = [
#         Project.objects.create(
#             name=fake.bs().capitalize(),
#             description=fake.paragraph(),
#             start_date=fake.date_this_year()
#         )
#         for _ in range(5)
#     ]

#     employees = [
#         Employee.objects.create(
#             name=fake.name(),
#             email=fake.email()
#         )
#         for _ in range(10)
#     ]

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

#     for task in tasks:
#         TaskDetail.objects.create(
#             task=task,
#             assigned_to=", ".join(emp.name for emp in task.assigned_to.all()),
#             priority=random.choice(['H', 'M', 'L']),
#             notes=fake.paragraph()
#         )

#     print("Database populated successfully!")

# if __name__ == "__main__":
#     populate_db()

import os
import django
import sys
import random
from datetime import date, timedelta

# ----- 1. Set project path -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# ----- 2. Setup Django -----
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

# ----- 3. Import models -----
from tasks.models import Project, Tasks, TaskDetail
from users.models import CustomUser
from faker import Faker


def random_date():
    return date.today() + timedelta(days=random.randint(1, 60))


def populate_db():
    fake = Faker()

    # ---------- Projects ----------
    projects = [
        Project.objects.create(
            name=fake.bs().capitalize(),
            description=fake.paragraph(),
            start_date=fake.date_this_year()
        )
        for _ in range(5)
    ]

    # ---------- Users ----------
    users = []
    for i in range(10):
        username = f"user{i+1}"
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                "email": fake.email(),
                "bio": fake.text()
            }
        )
        if created:
            user.set_password("12345678")
            user.save()
        users.append(user)

    # ---------- Tasks ----------
    tasks = []
    for _ in range(20):
        task = Tasks.objects.create(
            project=random.choice(projects),
            title=fake.sentence(),
            description=fake.paragraph(),
            due_date=random_date(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            is_completed=random.choice([True, False])
        )

        # ManyToMany → CustomUser
        task.assigned_to.set(
            random.sample(users, random.randint(1, 3))
        )

        tasks.append(task)

    # ---------- Task Details (OneToOne) ----------
    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            assigned_to=", ".join(user.username for user in task.assigned_to.all()),
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )

    print("✅ Database populated successfully!")


if __name__ == "__main__":
    populate_db()
