from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    # link to another model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # define text with limited number of characters
    title = models.CharField(max_length=200)
    # long text without a limit
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class CLIP(models.Model):

    bar_choices = [
        ("barcode_set1.csv", "barcode_set1.csv"),
    ]
    chrom_choices = [
        ("hg38.chrom.sizes", "hg38.chrom.sizes"),
        ("hg19.chrom.sizes", "hg19.chrom.sizes"),
    ]
    star_choices = [
        ("star_2_7_gencode29_sjdb", "star_2_7_gencode29_sjdb"),
        ("star_2_7_6a_release6_sjdb", "star_2_7_6a_release6_sjdb"),
    ]

    description = models.TextField(max_length=200, blank=True)
    barcode_file = models.CharField(max_length=25, choices=bar_choices, blank=True)
    chrom_sizes = models.CharField(max_length=50, choices=chrom_choices, blank=True)
    star_index = models.CharField(max_length=50, choices=star_choices, blank=True)
    umi_pattern = models.CharField(max_length=10, default="NNNNNNNNNN")
    # set default: 10 Ns
    fastqs = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.barcode_file


class Fastq(models.Model):

    adapt_choices = [
        ("InvRiL19_adapters.fasta", "InvRiL19_adapters.fasta"),
        ("InvRNA1.fasta", "InvRNA1.fasta"),
        ("InvRNA2.fasta", "InvRNA2.fasta"),
    ]

    title = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    adapter_path = models.CharField(max_length=50, choices=adapt_choices, blank=True)
    complete = models.BooleanField()

    def __str__(self):
        return self.title
