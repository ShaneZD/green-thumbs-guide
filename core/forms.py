from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import GardenPlant

class AddPlantForm(forms.ModelForm):
    class Meta:
        model = GardenPlant
        fields = ['plant', 'planted_date']
        widgets = {
            'planted_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class UpdatePlantCareForm(forms.ModelForm):
    class Meta:
        model = GardenPlant
        fields = ['last_watered', 'last_fertilized', 'last_pruned', 'notes']
        widgets = {
            'last_watered': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'last_fertilized': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'last_pruned': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }