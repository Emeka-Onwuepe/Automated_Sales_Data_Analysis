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
        dataset = None
        # check if user browser exists
        try:
                user_id = User_id.objects.get(user_id = request.POST['user_id'])
        except User_id.DoesNotExist:
                user_id = User_id.objects.create(user_id = request.POST['user_id'])
        # check for double submission
        
        try:
            dataset = Dataset.objects.get(dataset_id = request.POST['dataset_id'] )
            form = DataSetForm(data= request.POST,files=request.FILES,instance = dataset)
            
        except Dataset.DoesNotExist:     
            dataset = Dataset.objects.create(user_id = user_id)
            form = DataSetForm(data= request.POST,files=request.FILES,instance = dataset)
        #     save form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('process:classifyView',
                        kwargs={"user_id":dataset.user_id,"dataset_id":dataset.dataset_id}))          
    return render(request,'home/home.html',{"form":form})
