from django import forms
from .models import MyUser

# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['file']

