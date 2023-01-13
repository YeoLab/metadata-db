from django.core.validators import RegexValidator
import yaml
import os

ALPHANUMERICUNDERSCORE = RegexValidator
(r'^[0-9a-zA-Z_]*$', 'Only alphanumeric characters are allowed.')

with open('form_builder/refs/refs.yaml', 'r') as stream:
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
