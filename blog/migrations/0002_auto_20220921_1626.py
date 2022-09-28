# Generated by Django 3.2.15 on 2022-09-21 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clip',
            name='barcode_file',
            field=models.CharField(blank=True, choices=[], max_length=25),
        ),
        migrations.AlterField(
            model_name='fastq',
            name='adapter_path',
            field=models.CharField(blank=True, choices=[('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta', '/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRiL19_adapters.fasta'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA1_adapters.fasta', '/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA1_adapters.fasta'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA2_adapters.fasta', '/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA2_adapters.fasta'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA3_adapters.fasta', '/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA3_adapters.fasta'), ('/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA4_adapters.fasta', '/projects/ps-yeolab4/software/eclip/0.7.1/examples/inputs/InvRNA4_adapters.fasta')], max_length=90),
        ),
    ]