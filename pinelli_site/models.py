from django.db import models

# Create your models here.
class Product(models.Model):# model for table in sql with name Product
    title=models.CharField(max_length=100)#create field called title that is varchar(50)
    price=models.FloatField()
    description=models.TextField()
    category=models.CharField(max_length=20)
    sub_category=models.CharField(max_length=20)
    indoors=models.BooleanField()
    image=models.ImageField(upload_to="static/images")

class Rating(models.Model):
    username=models.CharField(max_length=150)
    product_id=models.IntegerField()
    rating=models.FloatField()
