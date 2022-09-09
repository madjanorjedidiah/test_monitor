from django import forms
from monitor.models import *



class UserBioForm(forms.ModelForm):
    class Meta:
        model = UserIdentity
        fields = "__all__"
        exclude = (
            "password", 
            "last_login", 
            "is_superuser", 
            "username",
            "is_staff",
            "is_active",
            "date_joined")


