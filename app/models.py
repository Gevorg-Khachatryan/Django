from django.db import models

# Create your models here.
class Users(models.Model):

    name=models.CharField(max_length=100)
    usrname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    emailconf=models.BooleanField(default=False)
    photo = models.ImageField(upload_to='image/',default='default_user_photo.png')

class Products(models.Model):

    owner=models.IntegerField()
    name=models.CharField(max_length=100)
    info=models.CharField(max_length=1000)
    category=models.CharField(max_length=100,default='none')
    price=models.IntegerField()
    rating = models.IntegerField(default=0)

class Products_photos(models.Model):

    photo_id=models.IntegerField()
    photo=models.ImageField(upload_to='image/')

class Messages(models.Model):
    sender=models.IntegerField()
    receiver=models.IntegerField()
    message=models.CharField(max_length=1000)
    received=models.BooleanField(default=False)
    read=models.BooleanField(default=False)

class Basket(models.Model):
    owner=models.ForeignKey(Users, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)

class Comments(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000,default='No comments')