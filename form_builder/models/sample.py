from django.db import models
from django.contrib.auth.models import User
from .refs.refs_utils import *


class Sample(models.Model):
    '''
    Sample is an abstract class.
    '''
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.CharField(max_length=50, default="EXPERIMENT",
                                  validators=[ALPHANUMERICUNDERSCORE])
    sample = models.CharField(max_length=50, default="SAMPLE", validators=[
                              ALPHANUMERICUNDERSCORE])
    cells = models.CharField(max_length=50, default="",
                             validators=[ALPHANUMERICUNDERSCORE])
    replicate = models.IntegerField(default=1)

    class Meta:
        abstract = True  

