from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "location",
            "remote",
            "salary_min",
            "salary_max",
            "visa_sponsorship",
            "skills",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "w-full rounded-md border-gray-300"}),
            "skills": forms.TextInput(attrs={"placeholder": "Python, Django, React", "class": "w-full rounded-md border-gray-300"}),
            "title": forms.TextInput(attrs={"class": "w-full rounded-md border-gray-300"}),
            "location": forms.TextInput(attrs={"class": "w-full rounded-md border-gray-300"}),
            "salary_min": forms.NumberInput(attrs={"class": "w-full rounded-md border-gray-300"}),
            "salary_max": forms.NumberInput(attrs={"class": "w-full rounded-md border-gray-300"}),
            "remote": forms.CheckboxInput(attrs={"class": "rounded border-gray-300"}),
            "visa_sponsorship": forms.CheckboxInput(attrs={"class": "rounded border-gray-300"}),
        }

class JobSearchForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Job Title", "class": "w-full rounded-md border-gray-300"}))
    skills = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Skills (comma separated)", "class": "w-full rounded-md border-gray-300"}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Location", "class": "w-full rounded-md border-gray-300"}))
    salary_min = forms.IntegerField(label="Minimum Salary", required=False, widget=forms.NumberInput(attrs={"placeholder": "Min Salary", "class": "w-full rounded-md border-gray-300"}))
    salary_max = forms.IntegerField(label="Maximum Salary", required=False, widget=forms.NumberInput(attrs={"placeholder": "Max Salary", "class": "w-full rounded-md border-gray-300"}))
    remote = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "rounded border-gray-300"}))
    visa_sponsorship = forms.BooleanField(label="Visa Sponsorship", required=False, widget=forms.CheckboxInput(attrs={"class": "rounded border-gray-300"}))
