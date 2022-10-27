from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from data_sets.forms import DataSetForm
from data_sets.models import Dataset
from users.models import User_id

# Create your views here.
def homeView(request):
    form = DataSetForm()
    if request.method == "POST":
            user_id = None
            data = None
            try:
                    user_id = User_id.objects.get(user_id = request.POST['user_id'])
            except User_id.DoesNotExist:
                    user_id = User_id.objects.create(user_id = request.POST['user_id'])
            dataset = Dataset.objects.create(user_id = user_id)
            form = DataSetForm(data= request.POST,files=request.FILES,instance = dataset)
            if form.is_valid():
                data = form.save()
                return HttpResponseRedirect(reverse('process:classifyView',
                        kwargs={"user_id":data.user_id,"dataset_id":data.dataset_id}))          
    return render(request,'home/home.html',{"form":form})
