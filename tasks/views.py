from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from tasks.forms import TaskModelForm
from tasks.models import Employee, Tasks
from django.contrib.auth.decorators import user_passes_test, login_required

def home(request):
    return HttpResponse("Welcome to the task management System")
def onload(request):
    return HttpResponse("<h1>Hi there</h1>")
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def userdashboard(request):
     return render(request, 'user.html')
 
@user_passes_test(is_admin, login_url='no-permission')
def managerdashboard(request):
    tasks = Tasks.objects.all()

    total_task = tasks.count()
    task_completed = tasks.filter(status="COMPLETED").count()
    task_in_prog = tasks.filter(status="IN_PROGRESS").count()
    task_pending = tasks.filter(status="PENDING").count()

    context = {
        "tasks": tasks,
        "total": total_task,
        "completed": task_completed,
        "in_progress": task_in_prog,
        "pending": task_pending
    }

    return render(request, 'manager-dashboard.html', context)

@user_passes_test(is_admin, login_url='no-permission')
def create_task(request):
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return redirect('manager-dashboard')
    else:
        form = TaskModelForm()

    return render(request, "taskForm.html", {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def update_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    if request.method == "POST":
        form = TaskModelForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('manager-dashboard')
    else:
        form = TaskModelForm(instance=task)

    return render(request, "taskForm.html", {"form": form, "msg": "Update Task"})

@user_passes_test(is_admin, login_url='no-permission')
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    task.delete()  
    return redirect('manager-dashboard')