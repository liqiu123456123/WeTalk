from django import forms
from .models import MyUser


class UploadAvatarForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['avatar']