from django.db import models

# Create your models here.
class Data(models.Model):

    series_reference=models.CharField(max_length=30)
    period=models.CharField(max_length=30)
    data_value=models.CharField(max_length=30)
    status=models.CharField(max_length=30)
    units=models.CharField(max_length=30)
    subject=models.CharField(max_length=30)
    group=models.CharField(max_length=30)

class Files(models.Model):
    file=models.FileField()
