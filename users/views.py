from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from users.forms import EditProfileForm, RegisterForm, CustomRegistrationForm,LoginForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeFrom,CustomPasswordResetForm,CustomPasswordResetConfirmForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView,PasswordChangeView, PasswordChangeDoneView, PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView
from django.views.generic import TemplateView,UpdateView,ListView,FormView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

User = get_user_model()

def show_default(request):
    return HttpResponse("<h1>Welcome to task Management User pannel</h1>")

def is_admin(user):
    return user.groups.filter(name='Admin').exists()




'''  Sign Up CBV    '''
class SignUpView(FormView):
    template_name = "registration/register.html"
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        messages.success(self.request, 'A confirmation mail sent. Please check your email')
        return super().form_valid(form)




""" Creating Login system using CBV """
class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next if next_url else super().get_success_url()




""" custom password change View """
class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeFrom

@login_required
def sign_out(request):
    if request.method =='POST':
        logout(request)
        return redirect('home')
    
def activate_user(request, user_id, token):
   try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid ID or Token")
   except User.DoesNotExist:
       return HttpResponse("User does not exists")
   
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request,'admin/admin_dashboard.html',{"users":users})







'''
    Assign role CBV
'''
class AssignRoleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = AssignRoleForm
    template_name = 'admin/assign_role.html'
    pk_url_kwarg = 'user_id'

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        return redirect('no-permission')

    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        self.object.groups.clear()
        self.object.groups.add(role)
        messages.success(self.request, f"User {self.object.username} has been assigned to role {role.name}")
        return redirect('admin-dashboard')




'''     Create Group CBV   '''
class CreateGroupView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'admin/create_group.html'
    form_class = CreateGroupForm

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        return redirect('no-permission')

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"Group {group.name} created successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('create-group')


'''
Group list CBV
'''
class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        return redirect('no-permission')



class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = f"{user.first_name} {user.last_name}"
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context



class CustomResetPasswordView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request,'A reset email sent. Please check your email inbox')
        return super().form_valid(form)




class CustomResetPasswordConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request,'Password reset successful')
        return super().form_valid(form)
    



class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return redirect('profile')
        