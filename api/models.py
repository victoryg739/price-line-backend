from django.db import models


# Create your models here.

class Post(models.Model):
    town = models.TextField()
    flatType = models.TextField()
    flatModel = models.TextField()
    floorArea = models.TextField()
    floor = models.TextField()

    remainingLease = models.TextField()