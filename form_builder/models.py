from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import os
import yaml

ALPHANUMERICUNDERSCORE = RegexValidator(r'^[0-9a-zA-Z_]*$', 'Only alphanumeric characters are allowed.')


with open('form_builder/refs/refs.yaml', 'r') as stream:
    try:
        REFS = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        REFS = {}


def get_refs_choices(key, refs=REFS):
    """
    Returns a list of choices (tuples) according to a dictionary (refs)
    Args:
        refs: dictionary
        key: string

    Returns:

    """
    choices = []
    if key in refs.keys():
        for ref in refs[key]:
            for label, value in ref.items():
                choices.append((value, label))
    return choices


class CLIPManifest(models.Model):
    species_choices = get_refs_choices('species_choices')
    repeat_choices = get_refs_choices('repeat_choices')
    star_choices = get_refs_choices('star_choices')

    chrom_choices = []
    for tuple in star_choices:
        chrom_choices.append((os.path.join(tuple[0], 'chrNameLength.txt'), tuple[1] + " (must match genome)"))

    exclusion_choices = get_refs_choices('exclusion_choices')

    dataset = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=20, choices=species_choices, default=species_choices[0])
    repeatElementGenomeDir = models.CharField(max_length=120, choices=repeat_choices, default=repeat_choices[0])
    speciesGenomeDir = models.CharField(max_length=90, choices=star_choices, default=star_choices[0])
    chrom_sizes = models.CharField(max_length=120, choices=chrom_choices, default=chrom_choices[0])
    blacklist_file = models.CharField(max_length=120, choices=exclusion_choices, default=exclusion_choices[0])
    # set default: 10 Ns
    umi_pattern = models.CharField(max_length=20, default="NNNNNNNNNN")
    fastqs = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.dataset


class SkipperConfigManifest(models.Model):

    gff_choices = get_refs_choices("gff_choices")
    partition_choices = get_refs_choices("partition_choices")

    feature_choices = get_refs_choices("feature_choices")

    accession_rankings_choices = get_refs_choices("accession_rankings_choices")

    genome_choices = get_refs_choices("genome_choices")
    star_choices = get_refs_choices("star_choices")

    chrom_choices = []
    for tuple in star_choices:
        chrom_choices.append((os.path.join(tuple[0], 'chrNameLength.txt'), tuple[1] + " (must match genome)"))

    overdispersion_choices = get_refs_choices("overdispersion_choices")

    repeat_table_choices = get_refs_choices("repeat_table_choices")
    blacklist_choices = get_refs_choices("blacklist_choices")
    gene_sets_choices = get_refs_choices("gene_sets_choices")
    gene_set_reference_choices = get_refs_choices("gene_set_reference_choices")
    gene_set_distance_choices = get_refs_choices("gene_set_distance_choices")

    repo_path = models.CharField(max_length=200, default=REFS["skipper_repo_path"])
    manifest = models.CharField(max_length=200, default="manifest.csv")
    gff = models.CharField(max_length=200, choices=gff_choices, default=gff_choices[0])
    partition = models.CharField(max_length=200, choices=partition_choices, default=gff_choices[0])
    feature_annotations = models.CharField(max_length=200, choices=feature_choices, default=feature_choices[0])
    accession_rankings = models.CharField(max_length=200, choices=accession_rankings_choices, default=accession_rankings_choices[0])

    umi_size = models.IntegerField(default=10)
    default_informative_read = 1
    informative_read = models.IntegerField(default=default_informative_read)

    overdispersion_mode = models.CharField(max_length=200, choices=overdispersion_choices, default=overdispersion_choices[0])
    conda_dir = models.CharField(max_length=200, default="", blank=True)
    tool_dir = models.CharField(max_length=200, default=os.path.join(REFS["skipper_repo_path"], "tools"))

    exe_dir_path = os.path.dirname(REFS["skipper_repo_path"]) if not REFS["skipper_repo_path"].endswith('/') else os.path.dirname(REFS["skipper_repo_path"][:-1])
    exe_dir = models.CharField(max_length=200, default=exe_dir_path)

    star_dir = models.CharField(max_length=90, choices=star_choices, default=star_choices[0])
    r_exe = models.CharField(max_length=200, default=os.path.join(REFS["skipper_env_path"], 'bin', 'Rscript'))
    umicollapse_dir = models.CharField(max_length=200, default=os.path.join(exe_dir_path, 'UMICollapse'))
    java_exe = models.CharField(max_length=200, default=os.path.join(REFS["skipper_env_path"], 'bin', 'java'))
    genome = models.CharField(max_length=200, choices=genome_choices, default=genome_choices[0])
    chrom_sizes = models.CharField(max_length=200, choices=chrom_choices, default=chrom_choices[0][0])

    repeat_table = models.CharField(max_length=200, choices=repeat_table_choices, default=repeat_table_choices[0])

    blacklist = models.CharField(max_length=200, choices=blacklist_choices, default=blacklist_choices[0])
    gene_sets = models.CharField(max_length=200, choices=gene_sets_choices, default=gene_sets_choices[0])
    gene_set_reference = models.CharField(max_length=200, choices=gene_set_reference_choices, default=gene_set_reference_choices[0])
    gene_set_distance = models.CharField(max_length=200, choices=gene_set_distance_choices, default=gene_set_distance_choices[0])

    uninformative_read = models.IntegerField(default=3-default_informative_read)
    fastqs = models.CharField(max_length=200, blank=True)


class Fastq(models.Model):
    form_choices = [
        ("RnaseqSE", "RnaseqSE"),
        ("RnaseqPE", "RnaseqPE"),
        ("CLIP", "CLIP"),
        ("SKIPPER", "SKIPPER"),
    ]

    barcode_choices = [
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta",
            "InvRiL19_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA1_adapters.fasta",
            "InvRNA1_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA2_adapters.fasta",
            "InvRNA2_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA3_adapters.fasta",
            "InvRNA3_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA4_adapters.fasta",
            "InvRNA4_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA5_adapters.fasta",
            "InvRNA5_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA6_adapters.fasta",
            "InvRNA6_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA7_adapters.fasta",
            "InvRNA7_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA8_adapters.fasta",
            "InvRNA8_adapters.fasta (eCLIP)"
        ),
        (
            "/projects/ps-yeolab4/software/skipper/8674296/examples/InvRiL19.fasta",
            "InvRiL19.fasta (SKIPPER)"
        ),

    ]

    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.CharField(max_length=20, choices=form_choices)
    experiment = models.CharField(max_length=50, default="EXPERIMENT", validators=[ALPHANUMERICUNDERSCORE])
    sample = models.CharField(max_length=50, default="SAMPLE", validators=[ALPHANUMERICUNDERSCORE])
    cells = models.CharField(max_length=50, default="", validators=[ALPHANUMERICUNDERSCORE])

    ip_title = models.CharField(max_length=50, default="IP", validators=[ALPHANUMERICUNDERSCORE])
    ip_path = models.CharField(max_length=255, default="")
    ip_adapter_path = models.CharField(max_length=255, choices=barcode_choices, default=barcode_choices[0])
    ip_rep = models.IntegerField(default=1)
    ip_complete = models.BooleanField()

    sminput_title = models.CharField(max_length=50, default="SMINPUT", validators=[ALPHANUMERICUNDERSCORE])
    sminput_path = models.CharField(max_length=255, default="")
    sminput_adapter_path = models.CharField(max_length=255, choices=barcode_choices, default=barcode_choices[0])
    sminput_rep = models.IntegerField(default=1)
    sminput_complete = models.BooleanField()

    def __str__(self):
        return self.ip_title

    
class RnaseqSE(models.Model):
    species_choices = [('hg19', 'hg19'), ('mm10', 'mm10'), ('GRCh38', 'GRCh38')]
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
    speciesGenomeDir = models.CharField(max_length=90, choices=species_genome_choices)
    repeatElementGenomeDir = models.CharField(max_length=120, choices=repeat_choices)
    b_adapters = models.CharField(max_length=120, choices=adapter_choices)
    direction = models.CharField(max_length = 2, choices=direction_choices, default="r")
    fastqs = models.CharField(max_length=200, blank=True)

class RnaseqPE(models.Model):
    species_choices = [('hg19', 'hg19'), ('mm10', 'mm10'), ('GRCh38', 'GRCh38')]
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
    speciesGenomeDir = models.CharField(max_length=90, choices=species_genome_choices)
    repeatElementGenomeDir = models.CharField(max_length=120, choices=repeat_choices)
    b_adapters = models.CharField(max_length=120, choices=adapter_choices)
    direction = models.CharField(max_length = 2, choices=direction_choices, default="r")
    fastqs = models.CharField(max_length=200, blank=True)


