#!/bin/env python3

import pandas as pd
import xlrd
from neural_network import NeuralNetwork
import numpy as np
from heapq import nlargest

# Initialization
nn = NeuralNetwork(402, 50, 134)
learningRate = 0.1
df = pd.read_excel('data.xlsx')

# Data preparation
disease_list = df.Disease.to_list()
# Removing spaces created from excel
while "\xa0" in disease_list: disease_list.remove("\xa0")

occurance_list = df.Count_of_Disease_Occurrence.to_list()
# Removing spaces created from excel
while "\xa0" in occurance_list: occurance_list.remove("\xa0")

symptom_list = df.Symptom.to_list()
# Remove duplicates
symptom_list_filter = list(set(symptom_list))

# print(disease_list)
# print(symptom_list_filter)
# print(occurance_list)

#-- Prepare Input and target vector and feed it to NN for training --#
def training():
    print("Training Data Started")

    # No of times data set is training to NN
    loop = 50
    for l in range(loop):
        # All inputs and target except last one
        print(str(int(l/70*100))+"% completed")
        tmpInput = df.Disease.to_list()
        tmpInd = 0
        for i in tmpInput:
            if( i!= "\xa0"):
                inputVec = np.zeros(shape=(402,1))
                targetVec = np.zeros(shape=(134,1))
                ind = tmpInput.index(i)
                if (ind != 0):
                    inputList = symptom_list[tmpInd:ind]
                    for k in inputList:
                        vecInd = symptom_list_filter.index(k)
                        inputVec[vecInd] += 1
                    targetVec[disease_list.index(i)-1] = 1
                    nn.trainSVLearing(inputVec,targetVec,learningRate)
                    tmpInd = ind

        # Last Inputs and Target
        inputVec = np.zeros(shape=(402,1))
        targetVec = np.zeros(shape=(134,1))
        j = len(symptom_list)
        inputList = symptom_list[tmpInd:j]
        for k in inputList:
            vecInd = symptom_list_filter.index(k)
            inputVec[vecInd] += 1
        targetVec[-1:] = 1
        nn.trainSVLearing(inputVec,targetVec,learningRate)
    print("------- TRAINING COMPLETE -------")

def getData():
    # Function that generates common symptoms and pass it as well 
    # all the symptoms from data set
    from collections import Counter
    c = Counter(symptom_list) 

    # Select only first 20
    words = c.most_common(20)
    top_symptom = []
    for i in words:
        top_symptom.append(i[0])
    return(top_symptom,symptom_list_filter)

def predict(checked_list):
    inputVec = np.zeros(shape=(402,1))
    for item in checked_list:
        if(item!=""):
            ind = symptom_list_filter.index(item)
            inputVec[ind]=1
    result = nn.feedForward(inputVec)
    result_norm = [float(i)/sum(result) for i in result]
    top_prediction = nlargest(8, enumerate(result_norm), key=lambda x: x[1])
    predicted_values = [[0 for x in range(8)] for y in range(0)] 
    for i in top_prediction:
        tmp = disease_list[i[0]]
        dis = tmp.split('_', 1)[-1]
        percent = float(i[1])*100
        per = "%.5f" % percent + " %"
        predicted_values.append([dis,per])
    return predicted_values
        
# training()
# getData()
