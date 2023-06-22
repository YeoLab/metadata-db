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
        widgets = {
            'fastqs': HiddenInput,  # hide field since fastqs will be added 
                                    # using separate input
        }
