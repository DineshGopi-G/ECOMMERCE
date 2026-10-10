from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserSignUp(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Create a strong password"}))
    
    class Meta:
        model=User
        fields=['username']
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Choose a unique username"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
