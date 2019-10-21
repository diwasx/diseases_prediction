from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from subprocess import run, PIPE
import sys
from script import getData

# Create your views here.
def index(request):
    # Get common and all the symptoms from data set
    raw_data_common, raw_data_all = getData()

    # Split symptoms name by underscrore(_)
    common_symptom = []
    all_symptom = []
    for i in raw_data_common:
        tmp = i.split('_', 1)[-1]
        common_symptom.append(tmp)

    for i in raw_data_all:
        tmp = i.split('_', 1)[-1]
        all_symptom.append(tmp)

    data = list(zip(raw_data_common, common_symptom))
    data1 = list(zip(raw_data_all, all_symptom))

    if request.method =='POST' and 'train_data' in request.POST:
        # Run training function when Train button is clicked
        sys.path.append('..')
        from script import training
        training()

    if request.method =='POST' and 'predict_disease' in request.POST:
        # Get symptoms list and prepare them for input
        checked_list = request.POST.getlist('checks[]')
        symptoms_set = request.POST.get("symptoms_field")
        symptoms_list = symptoms_set.split(",")
        merged_list = symptoms_list + checked_list
        merged_list = list(set(merged_list))
        print("\nInput are : \n",merged_list)

        # When no symptoms is selected
        if all('' == s or s.isspace() for s in merged_list):
            print("\nInput is empty:\n")
            return render(request, "home.html", {"data": data, "data1": data1})

        # Feed input list to predict function to generate prediction output
        sys.path.append('..')
        from script import predict
        values =  predict(merged_list)
        print("\nOutput are:\n",values,"\n")
        return render(request, "home.html", {"data": data, "data1": data1, "predicted_diseases": values})

    return render(request, "home.html", {"data": data, "data1": data1})
