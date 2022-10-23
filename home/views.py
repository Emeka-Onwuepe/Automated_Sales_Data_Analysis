from django.shortcuts import render
from data_sets.forms import DataSetForm
import pandas as pd

# Create your views here.
def homeView(request):
    form = DataSetForm()
    if request.method == "POST":
            form = DataSetForm(data= request.POST,files=request.FILES)
            if form.is_valid():
                data = form.save()
                print(data)
    
    return render(request,'home/home.html',{"form":form})
