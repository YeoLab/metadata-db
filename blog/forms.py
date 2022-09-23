# import django forms
from django import forms
# import Post model
from django.forms import HiddenInput, Select

from .models import Post, CLIPManifest, Fastq


# is a ModelForm
class PostForm(forms.ModelForm):
# which model should be used to create this form
    class Meta:
        model = Post
        # which fields end up in the form
        fields = ('title', 'text',)


class CLIPManifestForm(forms.ModelForm):
    class Meta:
        model = CLIPManifest
        fields = (
            'dataset',
            'description',
            'species',
            'chrom_sizes',
            'barcode_file',
            'speciesGenomeDir',
            'repeatElementGenomeDir',
            'blacklist_file',
            'umi_pattern',
            'fastqs',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'fastqs': HiddenInput,  # hide field since fastqs will be added using separate input
            'barcode_file': HiddenInput
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