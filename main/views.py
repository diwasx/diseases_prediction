from django.shortcuts import render
from django.http import HttpResponse
from subprocess import run, PIPE
import sys
from script import getData

# Create your views here.

def index(request):
    # return HttpResponse("<h1>Hello, world. You're at the polls index.</h1>")
    raw_data = getData()

    common_symptom = []
    for i in raw_data:
        tmp = i.split('_', 1)[-1]
        common_symptom.append(tmp)
    # print(common_symptom)
    # print(raw_data)
    data = list(zip(raw_data, common_symptom))
    print(data)

    if request.method =='POST' and 'train_data' in request.POST:
        sys.path.append('..')
        from script import training
        training()
    # return render(request, "home.html", {})
    return render(request, "home.html", {"data": data})
