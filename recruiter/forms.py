from django import forms

class ContactCandidateForm(forms.Form):
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'w-full ml-2'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full', 'rows': 6, 'style': 'margin-left:0.5rem;'}))
