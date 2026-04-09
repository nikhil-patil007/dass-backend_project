from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number= models.CharField(max_length=20, default="", blank=True, null=True)
    name = models.CharField(max_length=100,default="",blank=True,null=True)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def __str__(self):
    #     return "{}".format(self.email)
