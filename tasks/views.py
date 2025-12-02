from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Tasks

# Create your views here.
def onload(request):
    return HttpResponse("<h1>Hi there</h1>")
def home(request):
    return HttpResponse("Welcome to the task management System")
def userdashboard(request):
    return render(request,'user.html')
def managerdashboard(request):
    tasks = Tasks.objects.all()
    total_task = tasks.count()
    task_completed = Tasks.objects.filter(status="COMPLETED").count()
    task_in_prog = Tasks.objects.filter(status="IN_PROGRESS").count()
    task_pending = Tasks.objects.filter(status="PENDING").count()

    context={
        "tasks":tasks,
        "total":total_task,
        "completed":task_completed,
        "in_progress":task_in_prog,
        "pending":task_pending
    }
    return render(request,'manager-dashboard.html',context)


def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"taskForm.html",{"form":form,"msg":"Task added successfully ✅"})
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Tasks.objects.create(title=title,description=description, due_date= due_date)
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task added successfully ✅")
    context = {
        "form":form
    }
    return render(request,"taskForm.html",context)