from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Author(User):
    class Meta:
        proxy = True

class Organization(models.Model):
    name = models.CharField(max_length=40, default='Name')
    author = models.ManyToManyField('Author')

    # aa = models.ForeignKey()

