# Generated by Django 3.2.14 on 2022-09-02 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CLIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
                ('barcode_file', models.CharField(choices=[('barcode_set1.csv', 'barcode_set1.csv')], max_length=25)),
                ('adapter_file', models.CharField(choices=[('InvRiL19_adapters.fasta', 'InvRiL19_adapters.fasta'), ('InvRNA1.fasta', 'InvRNA1.fasta'), ('InvRNA2.fasta', 'InvRNA2.fasta')], max_length=50)),
                ('chrom_sizes', models.CharField(choices=[('hg38.chrom.sizes', 'hg38.chrom.sizes'), ('hg19.chrom.sizes', 'hg19.chrom.sizes')], max_length=50)),
                ('star_index', multiselectfield.db.fields.MultiSelectField(choices=[('star_2_7_gencode29_sjdb', 'star_2_7_gencode29_sjdb'), ('star_2_7_6a_release6_sjdb', 'star_2_7_6a_release6_sjdb')], max_length=49)),
                ('umi_pattern', models.CharField(default='NNNNNNNNNN', max_length=10)),
                ('fastqs', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Fast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('complete', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
