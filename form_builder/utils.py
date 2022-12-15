# imports
from django.contrib import messages
from .models import Fastq
import yaml
from .views import *

def make_fastq(ip_fastq_path, ip_adapter_path, ip_rep, sminput_fastq_path,
               sminput_adapter_path, sminput_rep,
               cells, experiment, sample, submitter, request):
    '''
    Checks for valid FASTQs. Will output a message popup if fields are invalid 
    or incomplete or duplicates exist. For valid FASTQs, will create a FASTQ 
    Object.
    '''
    # complete fields
    if ip_fastq_path is None or ip_adapter_path is None or ip_rep is None or \
            sminput_fastq_path is None or sminput_adapter_path is None or \
            sminput_rep is None or cells is None or experiment is None or \
            sample is None or submitter is None:
        messages.error(
            request,
            f'Failed to add sample {sample} to the database \
                (are all fields completed?)'
        )

    # duplicate fastq paths
    elif len(Fastq.objects.filter(sample=sample, ip_path=ip_fastq_path,
                                  sminput_path=sminput_fastq_path)) > 0:
        messages.error(
            request,
            f'Fastq path: {ip_fastq_path} and {sminput_fastq_path} already \
                exists! Refusing to add to database.'
        )

    # duplicate reps for same sample
    elif len(Fastq.objects.filter(sample=sample, ip_rep=ip_rep,
                                  sminput_rep=sminput_rep,
                                  submitter=request.user)) > 0:
        messages.error(
            request,
            f'IP Replicate {ip_rep} and Size-matched Input Replicate \
                {sminput_rep} for sample {sample} already exists! Refusing to \
                add to database.'
        )

    # valid fastq
    else:
        # warning for duplicate ip rep
        if len(Fastq.objects.filter(sample=sample, ip_rep=ip_rep,
                                    submitter=request.user)) > 0:
            messages.warning(
                request,
                f'Warning - {sample} IP Replicate {ip_rep} exists in database \
                    (but with a different Size-matched Input replicate).'
            )
        # warning for duplicate input rep
        if len(Fastq.objects.filter(sample=sample, sminput_rep=sminput_rep,
                                    submitter=request.user)) > 0:
            messages.warning(
                request,
                f'Warning - {sample} Size-matched Input Replicate \
                    {sminput_rep} exists in database (but with a different \
                    IP replicate).'
            )
        # create fastq object with submitted fields
        Fastq.objects.create(
            submitter=submitter,
            experiment=experiment,
            sample=sample,
            ip_title=sample + "_CLIP_" + ip_rep,
            ip_rep=ip_rep,
            ip_path=ip_fastq_path,
            ip_adapter_path=ip_adapter_path,
            ip_complete=False,
            cells=cells,
            sminput_title=sample + "_SMINPUT_" + sminput_rep,
            sminput_rep=sminput_rep,
            sminput_path=sminput_fastq_path,
            sminput_adapter_path=sminput_adapter_path,
            sminput_complete=False
        )
    return
