from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'profile_image', 'bio', 'website', 'facebook', 'twitter', 'instagram', 'linkedin']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']
