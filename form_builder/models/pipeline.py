from django.db import models
from form_builder.refs.refs_utils import *
from form_builder.models.fastq import SingleEndFastq


class ClipperManifest(models.Model): #change to manifest instead of fastq
    dataset = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200, blank=True)
    species = models.CharField(
        max_length=20, choices=species_choices, default=species_choices[0])
    repeatElementGenomeDir = models.CharField(
        max_length=120, choices=repeat_choices, default=repeat_choices[0])
    speciesGenomeDir = models.CharField(
        max_length=90, choices=star_choices, default=star_choices[0])
    chrom_sizes = models.CharField(
        max_length=120, choices=chrom_choices, default=chrom_choices[0])
    blacklist_file = models.CharField(
        max_length=120, choices=exclusion_choices, default=exclusion_choices[0])
    fastqs = models.CharField(max_length=200, blank=True)

