from rest_framework import serializers
from . import models

class flatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.flatModel
        fields = ('town','flatType','flatModel','floorArea','floor','remainingLease')


class feedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.feedbackModel
        fields = ('name','email','message')
