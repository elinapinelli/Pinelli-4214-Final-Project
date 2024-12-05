from django import forms
from django.contrib.auth.models import User

# if the user changes something in their profile (to edit) it updates the changes
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
