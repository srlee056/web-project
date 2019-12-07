from django.db import models

class ebookData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

class eventData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    date = models.CharField(max_length=200)
    #date = models.DateTimeField()