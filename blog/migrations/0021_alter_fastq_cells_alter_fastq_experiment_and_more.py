# Generated by Django 4.1.1 on 2022-09-28 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_skipperconfigmanifest_accession_rankings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fastq',
            name='cells',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='experiment',
            field=models.CharField(default='EXPERIMENT', max_length=50),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='ip_adapter_path',
            field=models.CharField(default='/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta', max_length=255),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='ip_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='ip_title',
            field=models.CharField(default='IP', max_length=50),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='sample',
            field=models.CharField(default='SAMPLE', max_length=50),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='sminput_adapter_path',
            field=models.CharField(default='/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta', max_length=255),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='sminput_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='sminput_title',
            field=models.CharField(default='SMINPUT', max_length=50),
        ),
    ]
