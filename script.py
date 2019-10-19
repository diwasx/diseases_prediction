#!/bin/env python3

import pandas as pd
import xlrd
from neural_network import NeuralNetwork
import numpy as np

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

def training():
    print("Training Data Started")

    #-- Prepare Input and target vector and feed it to NN for training --#
    # All inputs and target except last one
    tmpInput = df.Disease.to_list()
    tmpInd = 0
    for i in tmpInput:
        if( i!= "\xa0"):
            inputVec = np.zeros(shape=(402,1))
            targetVec = np.zeros(shape=(134,1))
            ind = tmpInput.index(i)
            if (ind != 0):
                inputList = symptom_list[tmpInd:ind]
                # print (inputList)
                for k in inputList:
                    vecInd = symptom_list_filter.index(k)
                    inputVec[vecInd] += 1
                # print(inputVec,"\n")
                # print(disease_list.index(i))
                targetVec[disease_list.index(i)-1] = 1

                # print("INPUT IS \n",inputVec)
                # print("TARGET IS \n",targetVec)
                nn.trainSVLearing(inputVec,targetVec,learningRate)
                tmpInd = ind

    # Last Inputs and Target
    inputVec = np.zeros(shape=(402,1))
    targetVec = np.zeros(shape=(134,1))
    j = len(symptom_list)
    inputList = symptom_list[tmpInd:j]
    # print(inputList)
    for k in inputList:
        # print(k)
        vecInd = symptom_list_filter.index(k)
        # print(vecInd)
        inputVec[vecInd] += 1
    # print("INPUT IS \n",inputVec)
    targetVec[-1:] = 1
    # print("TARGET IS \n",targetVec)
    nn.trainSVLearing(inputVec,targetVec,learningRate)
    print("------- TRAINING COMPLETE -------")

def getData():
    # print(disease_list)
    # print(symptom_list)
    # print(symptom_list_filter)
    # print(occurance_list)

    from collections import Counter
    c = Counter(symptom_list) 
    # Select only first 20
    words = c.most_common(20)
    # print(words)
    top_symptom = []
    for i in words:
        # print(i[0])
        top_symptom.append(i[0])
    # print(top_symptom)
    return(top_symptom)

def predict(checked_list):
    # print("This is predicting function")
    # print(checked_list)
    inputVec = np.zeros(shape=(402,1))
    for item in checked_list:
        # print (item)
        ind = symptom_list_filter.index(item)
        # print(ind)
        inputVec[ind]=1
    # print(inputVec)
    result = nn.feedForward(inputVec)
    maxVal_pos = result.argmax(axis=0)
    print(maxVal_pos)
    print(result[maxVal_pos])
    predicted_disease = disease_list[int(maxVal_pos)]
    print(predicted_disease)
    
        
# training()
# getData()
