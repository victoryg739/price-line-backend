from django.db import models


# Create your models here.

class flatModel(models.Model):
    town = models.TextField()
    flatType = models.TextField()
    flatModel = models.TextField()
    floorArea = models.TextField()
    floor = models.TextField()
    remainingLease = models.TextField()

class feedbackModel(models.Model):
    name = models.TextField()
    email = models.TextField()
    message = models.TextField()
    
    # this will affect how the admin page views
    def __str__(self):
        return f'{self.name} , {self.email}'
