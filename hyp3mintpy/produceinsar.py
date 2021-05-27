from typing import no_type_check
from datetime import datetime

import numpy as np
from argparse import ArgumentParser

from hyp3_sdk import HyP3

def run_job(granule_list_file):
    
    hyp3 = HyP3(username='cirrusasf', password='Cumulus*181')

    job_name_prefix ='jz'

    #granule_list_file = "granule.txt"

    #read the granulelist file
    with open(granule_list_file) as f:
        lines = f.read().splitlines()

    num = len(lines)

    job_dic={}

    reference_id = lines[num-1]

    job_num = 1

    for i in range(num-2, 0, -1):

        secondary_id = lines[i]

        nowstr = datetime.now().strftime("%Y%m%d%H%M%S")

        nowstr = datetime.now().strftime("%y%m%d%H%M")

        job_name = "{prex}-ifm-{job_num}-{now}".format(prex=job_name_prefix, job_num = job_num, now = nowstr)

        job = hyp3.submit_insar_job(reference_id, secondary_id, job_name)

        job_num = job_num + 1

        job_dic[job_name] = job

    #check and download the job
    batch = hyp3.find_jobs()

    if not batch.complete():
        # to get updated information
        batch = hyp3.refresh(batch)

        # or to wait until completion and get updated information (which will take a fair bit)
        batch = hyp3.watch(batch)

    #download the jobs files
    batch.download_files()

    print("completed ...")

def main():
    parser = ArgumentParser()

    parser.add_argument('--gfilelist', required=True)

    args = parser.parse_args()

    filelist = args.gfilelist

    run_job(filelist)

    return


if __name__== "__main__":

    main()

