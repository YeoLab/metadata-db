from django.db import models
from form_builder.models.sample import Sample
from form_builder.refs.refs_utils import *

class Fastq(Sample):
    '''
    Fastq is an abstract class that extends the Sample class.
    '''
    title = models.CharField(max_length=50, default="", validators=[
                                ALPHANUMERICUNDERSCORE])
    path = models.CharField(max_length=255, default="")
    adapter_path = models.CharField(
        max_length=255, choices=barcode_choices, default=barcode_choices[0])
    three_prime_adapters_r1 = models.CharField(max_length=200, choices=
        three_prime_adapter_clip_choices + three_prime_adapter_skipper_choices, 
        default ="")
    five_prime_adapters_r1 = models.CharField(max_length=200, blank=True)
    umi = models.CharField(max_length=20, default="NNNNNNNNNN")

    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True  


class SingleEndFastq(Fastq):
    '''
    SingleEndFastq is a class that extends the Fastq class.
    '''
    read1 = models.CharField(max_length=255, default="")

