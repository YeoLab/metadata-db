from django.db import models
from models.sample import Sample
from .refs.refs_utils import *

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
        three_prime_adapter_clip_choices + three_prime_adapter_skipper_choices)
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


class PairedEndFastq(Fastq):
    '''
    PairedEndFastq is a class that extends the Fastq class.
    It includes an additional read. 
    '''
    read1 = models.CharField(max_length=255, default="")
    # str: path to read1 of fasta file required
    read2 = models.CharField(max_length=255, default="")
    # str: basename of 3' adapter file for read1 eg. "InvRNA2.fasta"

    # str: basename of 3' adapter file for read2 eg. "InvRNA2.fasta"
    three_prime_adapters_r2 = models.CharField(max_length=200,
                                            choices=three_prime_adapter_choices)
    # str: basename of 5' adapter file for read2
    # five_prime_adapters_r2 = 
