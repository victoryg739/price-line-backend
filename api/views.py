from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import feedbackModel
from api.serializers import *
import requests
import api.machineLearning as ml

# Create your views here.
@api_view(['POST'])
def post_flat_data(request):
    serializer = flatSerializer(data=request.data)

    if serializer.is_valid():
        #serializer.save() will save the data into the database 
        #serializer.save()
        #if flat model or flatType is any 
        govDataUrl ='https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&sort=month desc&filters={"town":"'+ serializer.data['town'] + '"'
        extraUrl = ""
        if(serializer.data['flatType'] != "Any"):
            extraUrl =  ',"flat_type": "' + serializer.data['flatType'] + '"'
        
        if(serializer.data['flatModel'] !=  "Any"):
            extraUrl = extraUrl + ',"flat_model": "' + serializer.data['flatModel'] + '"'
        govDataUrl = govDataUrl + extraUrl +"}"
        
        response = requests.get(govDataUrl)
        data =  response.json()

        data = filter(data,serializer.data['floorArea'],serializer.data['remainingLease'],serializer.data['floor'])

        data["result"]["records"] = data["result"]["records"][0:10]
        data["result"]["resaleValue"] = ml.runMl(request.data)
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def filter(datas,floorArea,lease,floor):

    #remember recordData is a pointer to datas["result"]["records"] 
    recordDatas = datas["result"]["records"]
    #if empty list 
    if not recordDatas:
        return datas

    
    #filter the dropdown floorArea
    if(floorArea == "< 40 SQM" or floorArea == "> 169 SQM"):
        partsFloorArea = floorArea.split(" ")
        lowFloorArea = 0
        highFloorArea = int(partsFloorArea[1].split(" ")[0])
    elif(floorArea != "Any"):
        # partFloorArea[0] will be "70", partFloorArea[1] will be "79 SQM"
        partsFloorArea = floorArea.split(" - ")
        lowFloorArea = int(partsFloorArea[0])
        highFloorArea =  int(partsFloorArea[1].split(" ")[0])
    
    #filter the dropdown remainingLease
    if(lease == "< 50 YEARS" or lease == "> 89 YEARS"):    
        partsLease = lease.split(" ")
        lowLease = 0
        highLease = int(partsLease[1].split(" ")[0])
    elif(lease != "Any"):
        partsLease = lease.split(" - ")
        lowLease = int(partsLease[0])
        highLease =  int(partsLease[1].split(" ")[0])

    #filter the dropdown floor
    if(floor == "> 30th"):    
        partsFloor = floor.split(" ")
        highFloor= int(partsFloor[1].split("th")[0])
    elif(floor != "Any"):
        if("st" in floor):
            partsFloor = floor.split("st - ")
            lowFloor = int(partsFloor[0])
            highFloor = int(partsFloor[1].split("th")[0])
        else:
            partsFloor = floor.split("th - ")
            lowFloor = int(partsFloor[0])
            highFloor = int(partsFloor[1].split("th")[0])


    #how to solve indexing when removing, can loop backwards or [:] which creates a new list
    for recordData in recordDatas[:]:
 
         #need to split as data is string has years and mths 92 year 11 months -> take years only
        dataLease = int(recordData["remaining_lease"].split(" ")[0])
     
        #need to split data for floor given format is:"storey_range": "22 TO 24"
        dataFloorLow = int(recordData["storey_range"].split(" TO ")[0])
        dataFloorHigh = int(recordData["storey_range"].split(" TO ")[1])
        

        #remove one time dont need check alr
        if(floorArea == "> 169 SQM" ):
            if(floorArea != "Any" and not(int(recordData["floor_area_sqm"]) > highFloorArea)):
                datas["result"]["records"].remove(recordData)
                continue
        elif(floorArea != "Any" and not(lowFloorArea <= int(recordData["floor_area_sqm"]) and int(recordData["floor_area_sqm"]) <= highFloorArea) ):
            datas["result"]["records"].remove(recordData)
            continue
    
        if(lease == "> 89 YEARS" ):
            if(lease != "Any" and not(dataLease > highLease)):
                datas["result"]["records"].remove(recordData)     
                continue   
        elif(lease != "Any" and not(lowLease <= dataLease and dataLease <= highLease)):
            datas["result"]["records"].remove(recordData)
            continue

        if(floor == "> 30th"):
            if(floor != "Any" and not(dataFloorLow > highFloor and dataFloorHigh > highFloor)):
                datas["result"]["records"].remove(recordData)
                continue
        # 22 to 24 compared with 21st to 31th only need compare 22 with low and high 24 no need compare low agn
        elif(floor != "Any" and not(dataFloorLow >= lowFloor and dataFloorLow <= highFloor and dataFloorHigh <= highFloor)):
            datas["result"]["records"].remove(recordData)
            continue
    return datas

@api_view(['GET','POST'])
def get_post_feedback(request):
    if request.method == 'GET':
        feedback = feedbackModel.objects.all()
        serializer = feedbackSerializer(feedback, many=True)
        data = serializer.data
        for i, my_model in enumerate(feedback):
            data[i]['id'] = my_model.pk  # Include the primary key in the response data
        return Response(data)
    elif request.method == 'POST':
        serializer = feedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("ok",status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def deleteFeedback(request,pk):
        try:
            instance = feedbackModel.objects.get(pk=pk)
        except feedbackModel.DoesNotExist:
            return Response({'error': 'Record not found.'}, status=404)

        serializer = feedbackSerializer(instance)
        instance.delete()

        return Response(serializer.data, status=204)

