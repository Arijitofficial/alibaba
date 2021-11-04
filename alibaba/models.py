from django.db import models
# Create your models here.
class product(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,default="")
    category = models.CharField(max_length=20,default="")
    color = models.CharField(max_length=50,default="")
    price = models.CharField(max_length=10)
    desc = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    product_count = models.IntegerField(default=4)
    class meta:
        db_table = 'product'

class userinfo(models.Model):
    email=models.EmailField()
    pd=models.CharField(max_length=50)
    class meta:
        db_table='userinfo'

