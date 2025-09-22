from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import User

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1','password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )