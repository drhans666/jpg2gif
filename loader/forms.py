from django import forms
from django.forms import ModelForm
from .models import Upload, SizeChange


class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'
        widgets = {"upload": forms.FileInput(attrs={'multiple': True})}


class SizeChangeForm(ModelForm):
    class Meta:
        model = SizeChange
        fields = '__all__'
        widgets = {"size_file": forms.FileInput()}