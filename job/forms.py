from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "location", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5",
                "placeholder": "Enter job title"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5",
                "placeholder": "Describe the role and responsibilities..."
            }),
            "location": forms.TextInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5",
                "placeholder": "City, State or Remote"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            }),
        }
