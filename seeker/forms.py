from django import forms
from .models import JobSeekerProfile

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ["headline", "education", "work_experience", "skills", "location", "projects"]

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ["privacy"]
        widgets = {
            'privacy': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.privacy:
            # Create individual fields for each privacy setting
            for field_name, setting in self.instance.privacy.items():
                self.fields[f'privacy_{field_name}'] = forms.ChoiceField(
                    choices=JobSeekerProfile.Privacy.choices,
                    initial=setting,
                    label=f'{field_name.title()} Privacy'
                )
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.privacy is None:
            instance.privacy = {}
        
        # Update privacy settings from individual fields
        for field_name in ['headline', 'education', 'location', 'projects', 'work_experience', 'skills', 'links']:
            field_key = f'privacy_{field_name}'
            if field_key in self.cleaned_data:
                instance.privacy[field_name] = self.cleaned_data[field_key]
        
        if commit:
            instance.save()
        return instance