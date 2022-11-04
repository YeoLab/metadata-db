# import django forms
from django import forms
# import Post model
from django.forms import HiddenInput, Select

from .models import CLIPManifest, SkipperConfigManifest, Fastq, RnaseqFastq


class CLIPManifestForm(forms.ModelForm):
    class Meta:
        model = CLIPManifest
        fields = (
            'dataset',
            'description',
            'species',
            'chrom_sizes',
            'speciesGenomeDir',
            'repeatElementGenomeDir',
            'blacklist_file',
            'umi_pattern',
            'fastqs',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'fastqs': HiddenInput,  # hide field since fastqs will be added using separate input
        }


class SkipperConfigManifestForm(forms.ModelForm):
    class Meta:
        model = SkipperConfigManifest
        fields = (
            'repo_path',
            'manifest',
            'gff',
            'partition',
            'feature_annotations',
            'accession_rankings',
            'umi_size',
            'informative_read',
            'overdispersion_mode',
            'conda_dir',
            'tool_dir',
            'exe_dir',
            'star_dir',
            'r_exe',
            'umicollapse_dir',
            'java_exe',
            'genome',
            'chrom_sizes',
            'repeat_table',
            'blacklist',
            'gene_sets',
            'gene_set_reference',
            'gene_set_distance',
            'uninformative_read',
            'fastqs',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'fastqs': HiddenInput,  # hide field since fastqs will be added using separate input
            'repo_path': HiddenInput,
            'informative_read': HiddenInput,  # hide field since fastqs will be added using separate input
            'uninformative_read': HiddenInput,
            'conda_dir': HiddenInput,
            'tool_dir': HiddenInput,
            'exe_dir': HiddenInput,
            'r_exe': HiddenInput,
            'umicollapse_dir': HiddenInput,
            'java_exe': HiddenInput,
        }


class FastqForm(forms.ModelForm):
    class Meta:
        model = Fastq
        fields = (
            'ip_title',
            'ip_path',
            'ip_adapter_path',
            'ip_complete',
            'sminput_title',
            'sminput_path',
            'sminput_adapter_path',
            'sminput_complete',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'ip_adapter_path': Select,
            'sminput_adapter_path': Select,
        }


class FastqSkipperForm(forms.ModelForm):
    class Meta:
        model = Fastq
        fields = (
            'cells',
            'ip_title',
            'ip_path',
            'ip_adapter_path',
            'ip_complete',
            'sminput_title',
            'sminput_path',
            'sminput_adapter_path',
            'sminput_complete',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'ip_adapter_path': Select,
            'sminput_adapter_path': Select,
        }
    def clean(self):
        super(FastqSkipperForm)

class RnaseqFastqForm(forms.ModelForm):
    class Meta:
        model = RnaseqFastq
        fields = (
            'species',
            'chrom_sizes',
            'speciesGenomeDir',
            'repeatElementGenomeDir',
            'b_adapters',
            'direction',
        )