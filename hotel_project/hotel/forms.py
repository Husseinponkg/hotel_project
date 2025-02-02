from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    origin = forms.ChoiceField(choices=[
        ('african', 'Africa'),
        ('american', 'America'),
        ('european', 'Europe'),
        ('arabic', 'Arab'),
    ], required=True)

    class Meta:
        model = Profile
        fields = ['culture_choice', 'origin']

    def clean(self):
        cleaned_data = super().clean()
        culture_choice = cleaned_data.get('culture_choice')
        origin = cleaned_data.get('origin')

        origin_culture_map = {
            'african': 'African',
            'american': 'American',
            'european': 'European',
            'arabic': 'Arabic',
        }

        expected_culture = origin_culture_map.get(origin)

        if expected_culture and culture_choice != expected_culture:
            raise forms.ValidationError(f"Users from {origin} can only choose the {expected_culture} culture.")
        
        return cleaned_data