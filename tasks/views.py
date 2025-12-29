from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from tasks.models import Tasks
from tasks.forms import TaskModelForm


"""
  Admin Permission Mixin
"""

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        return redirect('no-permission')


"""
 Basic Views
""" 
 
class HomeView(View):
    def get(self, request):
        return render(request,'home.html')


class OnloadView(View):
    def get(self, request):
        return HttpResponse("<h1>Hi there</h1>")


class UserDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user.html')


"""
 Manager Dashboard
""" 
 
class ManagerDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'manager-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Tasks.objects.all()

        context['tasks'] = tasks
        context['total'] = tasks.count()
        context['completed'] = tasks.filter(status="COMPLETED").count()
        context['in_progress'] = tasks.filter(status="IN_PROGRESS").count()
        context['pending'] = tasks.filter(status="PENDING").count()

        return context


"""
 Create Task
""" 
 
class TaskCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Tasks
    form_class = TaskModelForm
    template_name = 'taskForm.html'
    success_url = reverse_lazy('manager-dashboard')


"""
 Update Task
""" 
 
class TaskUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Tasks
    form_class = TaskModelForm
    template_name = 'taskForm.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('manager-dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = 'Update Task'
        return context


"""
 Delete Task
""" 
 
class TaskDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Tasks
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('manager-dashboard')


"""
 Task Details
""" 
 
class TaskDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Tasks
    template_name = 'task_details.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
