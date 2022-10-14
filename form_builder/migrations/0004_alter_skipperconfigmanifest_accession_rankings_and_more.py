# Generated by Django 4.1.1 on 2022-10-11 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0003_alter_skipperconfigmanifest_feature_annotations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='accession_rankings',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/accession_type_ranking.txt', 'accession_type_ranking.txt')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/accession_type_ranking.txt', 'accession_type_ranking.txt'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='blacklist',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/encode3_eclip_blacklist.bed', 'encode3_eclip_blacklist.bed')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/encode3_eclip_blacklist.bed', 'encode3_eclip_blacklist.bed'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='exe_dir',
            field=models.CharField(default='/projects/ps-yeolab4/software/skipper/1.0.0/bin', max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='feature_annotations',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.features.tsv.gz', 'gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.features.tsv.gz'), ('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.hepg2_totalrna.gt1.tiled_partition.features.tsv.gz', 'gencode.v38.annotation.hepg2_totalrna.gt1.tiled_partition.features.tsv.gz'), ('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.hepg2_totalrna.gt1.tiled_partition.features.tsv.gz', 'gencode.v38.annotation.hepg2_totalrna.gt1.tiled_partition.features.tsv.gz'), ('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v41.annotation.tiled_partition.features.tsv.gz', 'gencode.v41.annotation.tiled_partition.features.tsv.gz')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.features.tsv.gz', 'gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.features.tsv.gz'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='gene_set_distance',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/encode3_go_terms.jaccard_index.rds', 'encode3_go_terms.jaccard_index.rds')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/encode3_go_terms.jaccard_index.rds', 'encode3_go_terms.jaccard_index.rds'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='gene_set_reference',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/encode3_go_terms.reference.tsv.gz', 'encode3_go_terms.reference.tsv.gz')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/encode3_go_terms.reference.tsv.gz', 'encode3_go_terms.reference.tsv.gz'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='gene_sets',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/c5.go.v7.5.1.symbols.gmt', 'c5.go.v7.5.1.symbols.gmt')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/c5.go.v7.5.1.symbols.gmt', 'c5.go.v7.5.1.symbols.gmt'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='gff',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.k562_totalrna.gt1.gff3.gz', 'gencode.v38.annotation.k562_totalrna.gt1.gff3.gz'), ('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.hepg2_totalrna.gt1.gff3.gz', 'gencode.v38.annotation.hepg2_totalrna.gt1.gff3.gz')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.k562_totalrna.gt1.gff3.gz', 'gencode.v38.annotation.k562_totalrna.gt1.gff3.gz'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='java_exe',
            field=models.CharField(default='/projects/ps-yeolab4/software/yeolabconda3/envs/skipper-1.0.0/bin/java', max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='partition',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.bed.gz', 'gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.bed.gz'), ('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.hepg2_totalrna.gt1.tiled_partition.bed.gz', 'gencode.v38.annotation.hepg2_totalrna.gt1.tiled_partition.bed.gz'), ('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.hek293t.gt1.tiled_partition.bed.gz', 'gencode.v38.annotation.hek293t.gt1.tiled_partition.bed.gz'), ('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v41.annotation.tiled_partition.bed.gz', 'gencode.v41.annotation.tiled_partition.bed.gz')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/gencode.v38.annotation.k562_totalrna.gt1.gff3.gz', 'gencode.v38.annotation.k562_totalrna.gt1.gff3.gz'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='r_exe',
            field=models.CharField(default='/projects/ps-yeolab4/software/yeolabconda3/envs/skipper-1.0.0/bin/Rscript', max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='repeat_table',
            field=models.CharField(choices=[('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/repeatmasker.grch38.tsv.gz', 'repeatmasker.grch38.tsv.gz')], default=('/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/repeatmasker.grch38.tsv.gz', 'repeatmasker.grch38.tsv.gz'), max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='repo_path',
            field=models.CharField(default='/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper', max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='tool_dir',
            field=models.CharField(default='/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/tools', max_length=200),
        ),
        migrations.AlterField(
            model_name='skipperconfigmanifest',
            name='umicollapse_dir',
            field=models.CharField(default='/projects/ps-yeolab4/software/skipper/1.0.0/bin/UMICollapse', max_length=200),
        ),
    ]