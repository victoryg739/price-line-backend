from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from api.serializers import PostSerializer
import requests

# Create your views here.
@api_view(['POST'])
def post_collection(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        govDataUrl ='https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&filters={"town":"'+ serializer.data['town'] + '","flat_type": "' + serializer.data['flatType'] +'","flat_model":"'+serializer.data['flatModel']+'"}'
        response = requests.get(govDataUrl)
        print(serializer.data['town'])
        print(govDataUrl)
        return Response(response.json(), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def test(request):
#     response = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&filters={"town": "ANG MO KIO","flat_type": "3 ROOM","flat_model":"Improved"}')
#     return JsonResponse(response.json())