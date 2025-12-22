from django.db import models
from django.utils import timezone
class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):  
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Tasks(models.Model):
    STATUS_CHOICE = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In progress'),
        ('COMPLETED', 'Completed')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):   
        return self.title


class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    Priority_Options = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    task = models.OneToOneField(Tasks, on_delete=models.CASCADE, related_name='details')
    assigned_to = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=Priority_Options, default=LOW)

    def __str__(self):  
        return f"Task details for {self.task.title}"