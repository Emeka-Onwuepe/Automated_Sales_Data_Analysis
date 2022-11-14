from django import forms
from .models import  Dataset

class DataSetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        exclude = ['zipfolder',"user_id","columns"]
        
        
class UploadZipFileForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['zipfolder']