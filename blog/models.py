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
    exclusion_choices = [
        (
            "/projects/ps-yeolab4/software/eclip/0.7.0/examples/inputs/eCLIP_blacklistregions.hg38liftover.bed.fixed.bed",
            "eCLIP_blacklistregions.hg38liftover.bed.fixed.bed"
        )
    ]
    dataset = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=20, choices=species_choices, default="GRCh38_v40")
    repeatElementGenomeDir = models.CharField(max_length=120, choices=repeat_choices, default="/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_homo_sapiens_repbase_fixed_v2")
    speciesGenomeDir = models.CharField(max_length=90, choices=star_choices, default="/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_gencode40_sjdb/")
    chrom_sizes = models.CharField(max_length=120, choices=chrom_choices, default="/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_gencode40_sjdb/chrNameLength.txt")
    blacklist_file = models.CharField(max_length=120, choices=exclusion_choices, default="/projects/ps-yeolab4/software/eclip/0.7.0/examples/inputs/eCLIP_blacklistregions.hg38liftover.bed.fixed.bed")
    # set default: 10 Ns
    umi_pattern = models.CharField(max_length=20, default="NNNNNNNNNN")
    fastqs = models.CharField(max_length=200, blank=True)
    barcode_file = models.CharField(max_length=120, choices=barcode_choices, blank=True)

    def __str__(self):
        return self.dataset


class SkipperManifest(models.Model):
    fastqs = models.CharField(max_length=200, blank=True)


class SkipperConfigManifest(models.Model):
    barcode_choices = [
        (
            "/projects/ps-yeolab4/software/skipper/8674296/examples/InvRiL19.fasta",
            "InvRiL19.fasta"
        ),
    ]
    skipper_repo_path = "/projects/ps-yeolab4/software/skipper/8674296/bin/skipper/"
    skipper_env_path = '/projects/ps-yeolab4/software/yeolabconda3/envs/skipper-8674296/'

    gff_choices = [
        (
            os.path.join(skipper_repo_path, "annotations/gencode.v38.annotation.k562_totalrna.gt1.gff3.gz"),
            "gencode.v38.annotation.k562_totalrna.gt1.gff3.gz"
        )
    ]
    partition_choices = [
        (
            os.path.join(skipper_repo_path, "annotations/gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.bed.gz"),
            "gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.bed.gz"
        )
    ]
    feature_choices = [
        (
            os.path.join(skipper_repo_path, "annotations/gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.features.tsv.gz"),
            "gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.features.tsv.gz"
        )
    ]
    accession_rankings_choices = [
        (
            os.path.join(skipper_repo_path,
                         "annotations/accession_type_ranking.txt"),
            "accession_type_ranking.txt"
        )
    ]
    genome_choices = [
        (
            "/projects/ps-yeolab4/genomes/GRCh38/chromosomes/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta",
            "GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta"
        )
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
    overdispersion_choices = [
        ('input', 'input'),
        ('clip', 'clip')
    ]
    repeat_table_choices = [
        (
            os.path.join(skipper_repo_path, "annotations/repeatmasker.grch38.tsv.gz"),
            "repeatmasker.grch38.tsv.gz"
        )
    ]
    blacklist_choices = [
        (
            os.path.join(skipper_repo_path, 'annotations', 'encode3_eclip_blacklist.bed'),
            'encode3_eclip_blacklist.bed'
        )
    ]
    gene_sets_choices = [
        (
            os.path.join(skipper_repo_path, 'annotations', 'c5.go.v7.5.1.symbols.gmt'),
            'c5.go.v7.5.1.symbols.gmt'
        )
    ]
    gene_set_reference_choices = [
        (
            os.path.join(skipper_repo_path, 'annotations', 'encode3_go_terms.reference.tsv.gz'),
            'encode3_go_terms.reference.tsv.gz'
        )
    ]
    gene_set_distance_choices = [
        (
            os.path.join(skipper_repo_path, 'annotations', 'encode3_go_terms.jaccard_index.rds'),
            'encode3_go_terms.jaccard_index.rds'
        )
    ]

    repo_path = models.CharField(max_length=200, default=skipper_repo_path)
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
    tool_dir = models.CharField(max_length=200, default=os.path.join(skipper_repo_path, "tools"))
    exe_dir = models.CharField(max_length=200, default=os.path.dirname(skipper_repo_path))

    star_dir = models.CharField(max_length=90, choices=star_choices, default=star_choices[0])
    r_exe = models.CharField(max_length=200, default=os.path.join(skipper_env_path, 'bin', 'Rscript'))
    umicollapse_dir = models.CharField(max_length=200, default=os.path.join(skipper_repo_path, 'UMICollapse'))
    java_exe = models.CharField(max_length=200, default=os.path.join(skipper_env_path, 'bin', 'java'))
    genome = models.CharField(max_length=200, choices=genome_choices, default=genome_choices[0])
    chrom_sizes = models.CharField(max_length=200, choices=chrom_choices, default=chrom_choices[0][0])

    repeat_table = models.CharField(max_length=200, choices=repeat_table_choices, default=repeat_table_choices[0])

    blacklist = models.CharField(max_length=200, choices=blacklist_choices, default=blacklist_choices[0])
    gene_sets = models.CharField(max_length=200, choices=gene_sets_choices, default=gene_sets_choices[0])
    gene_set_reference = models.CharField(max_length=200, choices=gene_set_reference_choices, default=gene_set_reference_choices[0])
    gene_set_distance = models.CharField(max_length=200, choices=gene_set_distance_choices, default=gene_set_distance_choices[0])

    uninformative_read = models.IntegerField(default=3-default_informative_read)
    barcode_file = models.CharField(max_length=120, choices=barcode_choices, default="/projects/ps-yeolab4/software/skipper/8674296/examples/InvRiL19.fasta")
    fastqs = models.CharField(max_length=200, blank=True)


class Fastq(models.Model):

    experiment = models.CharField(max_length=50, default="EXPERIMENT")
    sample = models.CharField(max_length=50, default="SAMPLE")
    cells = models.CharField(max_length=50, default="")

    ip_title = models.CharField(max_length=50, default="IP")
    ip_path = models.CharField(max_length=255, default="")
    ip_adapter_path = models.CharField(max_length=255, default="/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta")
    ip_rep = models.IntegerField(default=1)
    ip_complete = models.BooleanField()

    sminput_title = models.CharField(max_length=50, default="SMINPUT")
    sminput_path = models.CharField(max_length=255, default="")
    sminput_adapter_path = models.CharField(max_length=255, default="/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta")
    sminput_rep = models.IntegerField(default=1)
    sminput_complete = models.BooleanField()

    def __str__(self):
        return self.ip_title
