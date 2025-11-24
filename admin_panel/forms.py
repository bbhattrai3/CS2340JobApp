from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser']
        text_input_class = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        checkbox_class = 'h-4 w-4 text-blue-600 bg-gray-100 rounded border-gray-300'
        widgets = {
            'username': forms.TextInput(attrs={'class': text_input_class}),
            'email': forms.EmailInput(attrs={'class': text_input_class}),
            'first_name': forms.TextInput(attrs={'class': text_input_class}),
            'last_name': forms.TextInput(attrs={'class': text_input_class}),
            'role': forms.Select(attrs={'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm text-gray-900'}),
            'is_active': forms.CheckboxInput(attrs={'class': checkbox_class}),
            'is_staff': forms.CheckboxInput(attrs={'class': checkbox_class}),
            'is_superuser': forms.CheckboxInput(attrs={'class': checkbox_class}),
        }
