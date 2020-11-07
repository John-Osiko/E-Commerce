from django import forms
from .models import User

from .models import *

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "role"]