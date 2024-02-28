from django import forms
from .models import Room
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('contact_info',)


class CustomUserCreationForm(UserCreationForm):
    contact_info = forms.CharField(max_length=255, required=True, help_text='Enter your contact information.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'contact_info')

    def save(self, commit=True):
        user = super().save(commit=False)
        contact_info = self.cleaned_data['contact_info']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, contact_info=contact_info)
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')



class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['rent', 'location', 'photos', 'bhk', 'bathroom']