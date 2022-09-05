# import django forms
from django import forms
# import Post model
from django.forms import SelectMultiple, HiddenInput

from .models import Post, CLIP


# is a ModelForm
class PostForm(forms.ModelForm):
# which model should be used to create this form
    class Meta:
        model = Post
        # which fields end up in the form
        fields = ('title', 'text',)


class CLIPForm(forms.ModelForm):
    class Meta:
        model = CLIP
        fields = (
            'description',
            'barcode_file',
            'chrom_sizes',
            'star_index',
            'umi_pattern',
            'fastqs',
        )
        # TODO: find appropriate widget for each field.
        widgets = {
            'fastqs': HiddenInput  # hide field since fastqs will be added using separate input
        }