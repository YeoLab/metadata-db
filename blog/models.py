from django.conf import settings
from django.db import models
from django.utils import timezone
import os


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


class CLIPManifest(models.Model):
    barcode_choices = [
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta",
            "InvRiL19_adapters.fasta"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA1_adapters.fasta",
            "InvRNA1_adapters.fasta"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA2_adapters.fasta",
            "InvRNA2_adapters.fasta"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA3_adapters.fasta",
            "InvRNA3_adapters.fasta"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA4_adapters.fasta",
            "InvRNA4_adapters.fasta"
        ),
    ]
    star_choices = [
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_gencode40_sjdb/",
            "star_2_7_gencode40_sjdb/ (GRCh38)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_6a_gencode19_sjdb/",
            "star_2_7_6a_gencode19_sjdb/ (hg19)"
        ),
    ]
    chrom_choices = []
    for tuple in star_choices:
        chrom_choices.append((os.path.join(tuple[0], 'chrNameLength.txt'), tuple[1] + " (must match genome)"))
    repeat_choices = [
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_homo_sapiens_repbase_fixed_v2",
            "star_2_7_homo_sapiens_repbase_fixed_v2"
        ),
        (
            "/projects/ps-yeolab3/bay001/annotations/RepBase18.05/star_2_7_mus_musculus_repbase_fixed_v2",
            "star_2_7_mus_musculus_repbase_fixed_v2"
        )
    ]
    species_choices = [('hg19', 'hg19'), ('GRCh38_v40', 'GRCh38_v40')]

    description = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=20, choices=species_choices, blank=True)
    repeat_index = models.CharField(max_length=120, choices=repeat_choices, blank=True)
    star_index = models.CharField(max_length=90, choices=star_choices, blank=True)
    chrom_sizes = models.CharField(max_length=120, choices=chrom_choices, blank=True)

    umi_pattern = models.CharField(max_length=20, default="NNNNNNNNNN")
    # set default: 10 Ns
    fastqs = models.CharField(max_length=200, blank=True)
    barcode_file = models.CharField(max_length=120, choices=barcode_choices, blank=True)
    def __str__(self):
        return self.description[:100] + "..."


class Fastq(models.Model):

    ip_title = models.CharField(max_length=100)
    ip_path = models.CharField(max_length=100)
    ip_adapter_path = models.CharField(max_length=90)
    ip_complete = models.BooleanField()

    sminput_title = models.CharField(max_length=100)
    sminput_path = models.CharField(max_length=100)
    sminput_adapter_path = models.CharField(max_length=90)
    sminput_complete = models.BooleanField()

    def __str__(self):
        return self.ip_title
