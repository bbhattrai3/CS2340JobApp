from django import forms
from .models import SavedSearch

class ContactCandidateForm(forms.Form):
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'w-full ml-2'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full', 'rows': 6, 'style': 'margin-left:0.5rem;'}))

class SaveSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter a name for this search (e.g., "Python Developers in Atlanta")'
            })
        }
        labels = {
            'name': 'Search Name'
        }
