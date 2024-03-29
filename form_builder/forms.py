from django import forms
from django.forms import HiddenInput, Select
from .models import ClipperManifest, SingleEndFastq


class CLIPManifestForm(forms.ModelForm):
    class Meta:
        model = ClipperManifest
        fields = (
            'dataset',
            'description',
            'species',
            'repeatElementGenomeDir',
            'speciesGenomeDir',
            'chrom_sizes',
            'blacklist_file',
            'fastqs',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'fastqs': HiddenInput,  # hide field since fastqs will be added 
                                    # using separate input
        }

'''
class SkipperConfigManifestForm(forms.ModelForm):
    class Meta:
        model = SkipperManifest
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
            'fastqs': HiddenInput,      # hide field since fastqs will be added 
            'repo_path': HiddenInput,   # using separate input
            'informative_read': HiddenInput,  # hide field since fastqs will be 
            'uninformative_read': HiddenInput,# added using separate input
            'conda_dir': HiddenInput,
            'tool_dir': HiddenInput,
            'exe_dir': HiddenInput,
            'r_exe': HiddenInput,
            'umicollapse_dir': HiddenInput,
            'java_exe': HiddenInput,
        }


class FastqForm(forms.ModelForm):
    class Meta:
        model = SingleEndFastq
        fields = (
            'title',
            'path',
            'adapter_path',
            'three_prime_adapters_r1',
            'five_prime_adapters_r1',
            'umi',
            
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'adapter_path': Select,
        }

class FastqSkipperForm(forms.ModelForm):
    class Meta:
        model = SingleEndFastq
        fields = (
            'title',
            'path',
            'adapter_path',
            'three_prime_adapters_r1',
            'five_prime_adapters_r1',
            'umi',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'adapter_path': Select,
        }
    def clean(self):
        super(FastqSkipperForm)

class RnaseqForm(forms.ModelForm):
    class Meta:
        model = RnaSeqSingleEndFastq
        fields = (
            'species',
            'speciesChromSizes',
            'speciesGenomeDir',
            'repeatElementGenomeDir',
            'b_adapters',
            'direction',
        )
'''
