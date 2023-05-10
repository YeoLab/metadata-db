# Generated by Django 4.1.1 on 2023-05-10 22:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClipperManifest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.CharField(blank=True, max_length=20)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('species', models.CharField(choices=[('hg19', 'hg19'), ('mm10', 'mm10'), ('GRCh38_v40', 'GRCh38_v40')], default=('hg19', 'hg19'), max_length=20)),
                ('repeatElementGenomeDir', models.CharField(choices=[('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_homo_sapiens_repbase_fixed_v2', 'star_2_7_homo_sapiens_repbase_fixed_v2'), ('/projects/ps-yeolab3/bay001/annotations/RepBase18.05/star_2_7_mus_musculus_repbase_fixed_v2', 'star_2_7_mus_musculus_repbase_fixed_v2')], default=('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_homo_sapiens_repbase_fixed_v2', 'star_2_7_homo_sapiens_repbase_fixed_v2'), max_length=120)),
                ('speciesGenomeDir', models.CharField(choices=[('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_gencode40_sjdb/', 'star_2_7_gencode40_sjdb/ (GRCh38)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_6a_gencode19_sjdb/', 'star_2_7_6a_gencode19_sjdb/ (hg19)')], default=('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_gencode40_sjdb/', 'star_2_7_gencode40_sjdb/ (GRCh38)'), max_length=90)),
                ('chrom_sizes', models.CharField(choices=[('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_gencode40_sjdb/chrNameLength.txt', 'star_2_7_gencode40_sjdb/ (GRCh38) (must match genome)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_6a_gencode19_sjdb/chrNameLength.txt', 'star_2_7_6a_gencode19_sjdb/ (hg19) (must match genome)')], default=('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/star_2_7_gencode40_sjdb/chrNameLength.txt', 'star_2_7_gencode40_sjdb/ (GRCh38) (must match genome)'), max_length=120)),
                ('blacklist_file', models.CharField(choices=[('/projects/ps-yeolab4/software/eclip/0.7.0/examples/inputs/eCLIP_blacklistregions.hg38liftover.bed.fixed.bed', 'eCLIP_blacklistregions.hg38liftover.bed.fixed.bed'), ('/projects/ps-yeolab4/software/eclip/0.7.0/examples/inputs/eCLIP_blacklistregions.hg19.bed', 'eCLIP_blacklistregions.hg19.bed'), ('/projects/ps-yeolab4/software/eclip/0.7.0/examples/inputs/eCLIP_blacklistregions.noregion.bed', 'eCLIP_blacklistregions.noregion.bed')], default=('/projects/ps-yeolab4/software/eclip/0.7.0/examples/inputs/eCLIP_blacklistregions.hg38liftover.bed.fixed.bed', 'eCLIP_blacklistregions.hg38liftover.bed.fixed.bed'), max_length=120)),
                ('fastqs', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SingleEndFastq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment', models.CharField(default='EXPERIMENT', max_length=50, validators=[django.core.validators.RegexValidator])),
                ('sample', models.CharField(default='SAMPLE', max_length=50, validators=[django.core.validators.RegexValidator])),
                ('cells', models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator])),
                ('replicate', models.IntegerField(default=1)),
                ('title', models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator])),
                ('path', models.CharField(default='', max_length=255)),
                ('adapter_path', models.CharField(choices=[('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta', 'InvRiL19_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA1_adapters.fasta', 'InvRNA1_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA2_adapters.fasta', 'InvRNA2_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA3_adapters.fasta', 'InvRNA3_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA4_adapters.fasta', 'InvRNA4_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA5_adapters.fasta', 'InvRNA5_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA6_adapters.fasta', 'InvRNA6_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA7_adapters.fasta', 'InvRNA7_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA8_adapters.fasta', 'InvRNA8_adapters.fasta (eCLIP)'), ('/projects/ps-yeolab4/software/skipper/1.0.0/examples/InvRiL19.fasta', 'InvRiL19.fasta (SKIPPER)')], default=('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta', 'InvRiL19_adapters.fasta (eCLIP)'), max_length=255)),
                ('three_prime_adapters_r1', models.CharField(choices=[('InvRiL19_adapters.fasta', 'InvRiL19_adapters.fasta'), ('InvRNA1_adapters.fasta', 'InvRNA1_adapters.fasta'), ('InvRNA2_adapters.fasta', 'InvRNA2_adapters.fasta'), ('InvRNA3_adapters.fasta', 'InvRNA3_adapters.fasta'), ('InvRNA4_adapters.fasta', 'InvRNA4_adapters.fasta'), ('InvRNA5_adapters.fasta', 'InvRNA5_adapters.fasta'), ('InvRNA6_adapters.fasta', 'InvRNA6_adapters.fasta'), ('InvRNA7_adapters.fasta', 'InvRNA7_adapters.fasta'), ('InvRNA8_adapters.fasta', 'InvRNA8_adapters.fasta'), ('InvRiL19.fasta', 'InvRiL19.fasta'), ('InvRNA1.fasta', 'InvRNA1.fasta'), ('InvRNA2.fasta', 'InvRNA2.fasta'), ('InvRNA3.fasta', 'InvRNA3.fasta'), ('InvRNA4.fasta', 'InvRNA4.fasta'), ('InvRNA5.fasta', 'InvRNA5.fasta'), ('InvRNA6.fasta', 'InvRNA6.fasta'), ('InvRNA7.fasta', 'InvRNA7.fasta'), ('InvRNA8.fasta', 'InvRNA8.fasta')], default='', max_length=200)),
                ('five_prime_adapters_r1', models.CharField(blank=True, max_length=200)),
                ('umi', models.CharField(default='NNNNNNNNNN', max_length=20)),
                ('read1', models.CharField(default='', max_length=255)),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
