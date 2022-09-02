# import django forms
from pickle import FALSE
from sqlite3 import SQLITE_CREATE_INDEX
from django import forms
# import Post model
from .models import Fastq, Post, CLIP

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
        fields = ('description', 'barcode_file', 'adapter_file', 'chrom_sizes', 'star_index', 'umi_pattern', 'fastqs',)
    
    
    
    '''description = forms.CharField(widget=forms.Textarea)
    barcode_file = forms.ChoiceField(choices = [("barcode_set1.csv", "barcode_set1.csv")])
    adapter_file = forms.ChoiceField(choices = [("InvRiL19_adapters", "InvRiL19_adapters.fasta"), ("InvRNA1.fasta", "InvRNA1.fasta"), ("InvRNA2.fasta", "InvRNA2.fasta")])
    chrom_sizes = forms.ChoiceField(choices = [("hg38.chrom.sizes", "hg38.chrom.sizes"), ("hg19.chrom.sizes","hg19.chrom.sizes")])
    star_index = forms.ChoiceField(choices = [("star_2_7_gencode29_sjdb", "star_2_7_gencode29_sjdb"), ("star_2_7_6a_release6_sjdb", "star_2_7_6a_release6_sjdb")])
    # set default: 10 Ns, need 10 chars min/max
    umi_pattern = forms.CharField(min_length = 10, max_length = 10, empty_value="NNNNNNNNNN", required= False)
    fastqs = forms.CharField()'''