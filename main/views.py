from django.shortcuts import render
from django.http import HttpResponse
from subprocess import run, PIPE
import sys
from script import getData

# Create your views here.
def index(request):
    raw_data = getData()
    common_symptom = []
    for i in raw_data:
        tmp = i.split('_', 1)[-1]
        common_symptom.append(tmp)
    # print(common_symptom)
    # print(raw_data)
    data = list(zip(raw_data, common_symptom))
    # print(data)

    if request.method =='POST' and 'train_data' in request.POST:
        sys.path.append('..')
        from script import training
        training()

    if request.method =='POST' and 'predict_disease' in request.POST:
        # print("Predicting Disease")
        checked_list = request.POST.getlist('checks[]')
        # print(checked_list)

        sys.path.append('..')
        from script import predict
        predict(checked_list)

    return render(request, "home.html", {"data": data})
