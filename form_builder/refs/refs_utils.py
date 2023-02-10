from django.core.validators import RegexValidator
import yaml
import os


ALPHANUMERICUNDERSCORE = RegexValidator
(r'^[0-9a-zA-Z_]*$', 'Only alphanumeric characters are allowed.')

with open('refs.yaml', 'r') as stream:
    try:
        REFS = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        REFS = {}


def get_refs_choices(key, refs=REFS):
    '''
    Returns a list of choices (tuples) according to a dictionary (refs)
    Args:
        refs: dictionary
        key: string

    Returns:

    '''
    choices = []
    if key in refs.keys():
        for ref in refs[key]:
            for label, value in ref.items():
                choices.append((value, label))
    return choices

def get_chrome_choices(star_choices):
    chrom_choices = []
    for tuple in star_choices:
        chrom_choices.append((os.path.join(tuple[0], 'chrNameLength.txt'),
                              tuple[1] + " (must match genome)"))
    return chrom_choices

barcode_choices = get_refs_choices("barcodes_choices")
#three_prime_adapter_choices = get_refs_choices('three_prime_adapter_choices')
three_prime_adapter_clip_choices = get_refs_choices('three_prime_adapter_clip_choices')
three_prime_adapter_skipper_choices = get_refs_choices('three_prime_adapter_skipper_choices')
three_prime_adapter_choices = get_refs_choices('three_prime_adapter_choices')    
species_choices = get_refs_choices('species_choices')
repeat_choices = get_refs_choices('repeat_choices')
star_choices = get_refs_choices('star_choices')
chrom_choices = get_chrome_choices(star_choices)
exclusion_choices = get_refs_choices('exclusion_choices')
gff_choices = get_refs_choices("gff_choices")
partition_choices = get_refs_choices("partition_choices")
feature_choices = get_refs_choices("feature_choices")
accession_rankings_choices = get_refs_choices("accession_rankings_choices")
genome_choices = get_refs_choices("genome_choices")
star_choices = get_refs_choices("star_choices")
chrom_choices = get_chrome_choices(star_choices)
overdispersion_choices = get_refs_choices("overdispersion_choices")
repeat_table_choices = get_refs_choices("repeat_table_choices")
blacklist_choices = get_refs_choices("blacklist_choices")
gene_sets_choices = get_refs_choices("gene_sets_choices")
gene_set_reference_choices = get_refs_choices("gene_set_reference_choices")
gene_set_distance_choices = get_refs_choices("gene_set_distance_choices")