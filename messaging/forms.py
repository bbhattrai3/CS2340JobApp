from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    MESSAGE_TYPE_CHOICES = [
        ('internal', 'Internal Message (through platform)'),
        ('email', 'External Email (to seeker\'s email address)'),
    ]
    
    message_type = forms.ChoiceField(
        choices=MESSAGE_TYPE_CHOICES,
        initial='internal',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='How would you like to send this message?'
    )
    
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
