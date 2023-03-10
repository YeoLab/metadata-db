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
    #fastqs = models.ForeignKey(User, on_delete=models.CASCADE)
'''
    def get_three_prime_adapters(SingleEndFastq):
        return os.path.join(
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs",
            SingleEndFastq.three_prime_adapters_clip)
    
    def __str__(self):
        return self.dataset
'''


class SkipperManifest(SingleEndFastq):
    repo_path = models.CharField(
        max_length=200, default=REFS["skipper_repo_path"])
    manifest = models.CharField(max_length=200, default="manifest.csv")
    gff = models.CharField(
        max_length=200, choices=gff_choices, default=gff_choices[0])
    partition = models.CharField(
        max_length=200, choices=partition_choices, default=gff_choices[0])
    feature_annotations = models.CharField(
        max_length=200, choices=feature_choices, default=feature_choices[0])
    accession_rankings = models.CharField(
        max_length=200, choices=accession_rankings_choices,
        default=accession_rankings_choices[0])

    umi_size = models.IntegerField(default=10)
    default_informative_read = 1
    informative_read = models.IntegerField(default=default_informative_read)

    overdispersion_mode = models.CharField(
        max_length=200, choices=overdispersion_choices,
        default=overdispersion_choices[0])
    conda_dir = models.CharField(max_length=200, default="", blank=True)
    tool_dir = models.CharField(max_length=200, default=os.path.join(
        REFS["skipper_repo_path"], "tools"))

    exe_dir_path = os.path.dirname(REFS["skipper_repo_path"]) if not \
        REFS["skipper_repo_path"].endswith('/') \
        else os.path.dirname(REFS["skipper_repo_path"][:-1])
    exe_dir = models.CharField(max_length=200, default=exe_dir_path)

    star_dir = models.CharField(
        max_length=90, choices=star_choices, default=star_choices[0])
    r_exe = models.CharField(max_length=200, default=os.path.join(
        REFS["skipper_env_path"], 'bin', 'Rscript'))
    umicollapse_dir = models.CharField(
        max_length=200, default=os.path.join(exe_dir_path, 'UMICollapse'))
    java_exe = models.CharField(max_length=200, default=os.path.join(
        REFS["skipper_env_path"], 'bin', 'java'))
    genome = models.CharField(
        max_length=200, choices=genome_choices, default=genome_choices[0])
    chrom_sizes = models.CharField(
        max_length=200, choices=chrom_choices, default=chrom_choices[0][0])

    repeat_table = models.CharField(
        max_length=200, choices=repeat_table_choices,
        default=repeat_table_choices[0])

    blacklist = models.CharField(
        max_length=200, choices=blacklist_choices, default=blacklist_choices[0])
    gene_sets = models.CharField(
        max_length=200, choices=gene_sets_choices, default=gene_sets_choices[0])
    gene_set_reference = models.CharField(
        max_length=200, choices=gene_set_reference_choices,
        default=gene_set_reference_choices[0])
    gene_set_distance = models.CharField(
        max_length=200, choices=gene_set_distance_choices,
        default=gene_set_distance_choices[0])

    uninformative_read = models.IntegerField(
        default=3-default_informative_read)
    fastqs = models.CharField(max_length=200, blank=True)

    def get_three_prime_adapters(SingleEndFastq):
        return os.path.join(
            "/projects/ps-yeolab4/software/skipper/1.0.0/examples/inputs",
            SingleEndFastq.three_prime_adapters_skipper)


class RnaSeqManifest(SingleEndFastq):
    chrom_choices = [
        ('inputs/mm10.chrom.sizes', 'mm10.chrom.sizes'),
        ('inputs/hg19.chrom.sizes', 'hg19.chrom.sizes'),
        ('inputs/GRCh38.chrom.sizes', 'GRCh38.chrom.sizes')
    ]
    species_genome_choices = [
        ('inputs/star_2_4_0i_gencode19_sjdb', 'star_2_4_0i_gencode19_sjdb'),
        ('inputs/star_2_4_0i_gencode24_sjdb', 'star_2_4_0i_gencode24_sjdb'),
        ('inputs/star_2_4_0i_gencode29_sjdb', 'star_2_4_0i_gencode29_sjdb'),
        ('inputs/star_2_4_0i_mm10_sjdb', 'star_2_4_0i_mm10_sjdb')
    ]
    repeat_choices = [
        ('inputs/homo_sapiens_repbase_v2', 'homo_sapiens_repbase_v2'),
        ('inputs/mus_musculus_repbase_v2', 'mus_musculus_repbase_v2'),
        ('inputs/rat_rattus_repbase_v2', 'rat_rattus_repbase_v2')
    ]
    adapter_choices = [
        ('inputs/adapters.fasta', 'adapters.fasta')
    ]

    direction_choices = [
        ('r', 'r'),
        ('f', 'f')
    ]
    species = models.CharField(max_length=20, choices=species_choices)
    speciesChromSizes = models.CharField(max_length=200, choices=chrom_choices)
    speciesGenomeDir = models.CharField(
        max_length=90, choices=species_genome_choices)
    repeatElementGenomeDir = models.CharField(
        max_length=120, choices=repeat_choices)
    b_adapters = models.CharField(max_length=120, choices=adapter_choices)
    direction = models.CharField(
        max_length=2, choices=direction_choices, default="r")
    fastqs = models.CharField(max_length=200, blank=True)
    # add fields later, but similar to SEFastq

