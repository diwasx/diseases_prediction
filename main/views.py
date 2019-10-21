from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from subprocess import run, PIPE
import sys
from script import getData

# Create your views here.
def index(request):
    raw_data_common, raw_data_all = getData()
    common_symptom = []
    all_symptom = []
    for i in raw_data_common:
        tmp = i.split('_', 1)[-1]
        common_symptom.append(tmp)

    for i in raw_data_all:
        tmp = i.split('_', 1)[-1]
        all_symptom.append(tmp)

    # print(common_symptom)
    # print(raw_data_all)
    data = list(zip(raw_data_common, common_symptom))
    data1 = list(zip(raw_data_all, all_symptom))
    # print(data1)
    # print(symptom_all)

    if request.method =='POST' and 'train_data' in request.POST:
        sys.path.append('..')
        from script import training
        training()

    if request.method =='POST' and 'predict_disease' in request.POST:
        # print("Predicting Disease")
        checked_list = request.POST.getlist('checks[]')
        # print(checked_list)
        symptoms_set = request.POST.get("symptoms_field")
        # print(symptoms_set)
        symptoms_list = symptoms_set.split(",")
        # print(symptoms_list)
        merged_list = symptoms_list + checked_list
        merged_list = list(set(merged_list))
        print("\nInput are : \n",merged_list)

        sys.path.append('..')
        from script import predict
        # values =  predict(checked_list)
        # values =  predict(symptoms_list)

        if all('' == s or s.isspace() for s in merged_list):
            print("\nInput is empty:\n")
            return render(request, "home.html", {"data": data, "data1": data1})

        values =  predict(merged_list)
        print("\nOutput are:\n",values,"\n")
        return render(request, "home.html", {"data": data, "data1": data1, "predicted_diseases": values})

    return render(request, "home.html", {"data": data, "data1": data1})
