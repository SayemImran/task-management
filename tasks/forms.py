from django import forms
from tasks.models import Tasks

class TaskForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['project', 'title', 'description', 'due_date','assigned_to', 'status','asset'] # add ''
        widgets = {
            "title": forms.TextInput(attrs={
                'class': "border border-gray-600 rounded-md p-1 mb-3 w-full",
                'placeholder': "Enter the title name"
            }),
            'description': forms.Textarea(attrs={
                'class': "border border-gray-600 rounded-md p-1 h-10 mb-3 w-full",
                'placeholder': "Describe here about the task"
            }),
            "due_date": forms.SelectDateWidget,
            "assigned_to": forms.CheckboxSelectMultiple(),
            "status": forms.Select(),
            "asset": forms.ClearableFileInput(attrs={
            'class': "border border-gray-600 rounded-md p-1 mb-3 w-1/2",
            }),
        }

class TaskDetailModelForm(forms.ModelForm):
    pass