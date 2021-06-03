import os, sys
import re
import glob
import zipfile

import json
from typing import no_type_check
from datetime import datetime

import numpy as np

from argparse import ArgumentParser

from hyp3_sdk import HyP3

from hyp3lib.cutGeotiffs import cutFiles

def cutfiles(start_dir, pattern):
    '''
    clip off files in the start_dir and its sub-directories.

    '''
    files =[]
    for dir,_,_ in os.walk(start_dir):
        for item in pattern:
            files.extend(glob.glob(os.path.join(dir, item)))

    cutFiles(files)
    return

def run_job(granule_list_file, outdir):

    #read the EDL username and password from ~/.EDL.json
    home = os.path.expanduser("~")

    with open("{}/.EDL.json".format(home)) as f:
        data = json.load(f)
    
    hyp3 = HyP3(username=data['login'], password=data['password'])

    job_name_prefix ='jz'

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

        job = hyp3.submit_insar_job(reference_id, secondary_id, job_name,
                                    include_look_vectors=True, include_inc_map=True,
                                    include_los_displacement=True, include_dem=True,
                                    include_wrapped_phase=True)

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

    os.system("mkdir -p {}".format(outdir))

    os.chdir(outdir)

    batch.download_files()

    print("completed ...")


def config(template_file, data_dir, projectname):
    '''
    read in the template, produce the custom.txt and place inti inputs
    '''
    out_lines=[]
    with open(template_file) as file:
        lines = file.readlines()

    for line in lines:
        out_lines.append(line.replace('{DATA_DIR}', data_dir))

    outfile = open("{}/{}.cfg".format(data_dir, projectname), 'w')
    outfile.write("".join(out_lines))
    return



def get_sublist_via_pattern(lst, pattern_str):

    pattern = re.compile(pattern_str)

    return list(filter(pattern.search, lst))

def prep_data_struc(data_dir, config_file):
    '''
    organize the data into the format that mintpy requests
    '''
    #unzip zip files in current directory
    filelist = glob.glob("{}/*.zip".format(data_dir))
    # split the filelist into two lists
    p1 = "/[A-Z][0-9][A-Z][A-Z]_"
    
    filelist1 = get_sublist_via_pattern(filelist, p1)

    p2 = "/[A-Z][0-9][A-Z]_" 

    filelist2 = get_sublist_via_pattern(filelist, p2)

    for file in filelist1:
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(data_dir)


    # clip files

    cutfiles(data_dir, ["*.tif"])

    #copy a *.txt in one insar dirctory

    os.system("mkdir -p {}/DEM {}/inputs".format(data_dir, data_dir))
    
    prefix = filelist1[-1].split('.zip')[0]

    fileprefix = os.path.basename(prefix)

    txtfile = "{dir}/{fileprefix}.txt".format(dir = prefix, fileprefix = fileprefix)

    demfile = "{dir}/{fileprefix}_dem_clip.tif".format(dir = prefix, fileprefix = fileprefix)

    if os.path.exists(txtfile) and os.path.exists(demfile):

        cmd1 = "cp {file} {data_dir}/DEM/dem_clip.txt".format(file = txtfile, data_dir = data_dir)

        os.system(cmd1)

        cmd2 = "cp {file} {data_dir}/DEM/dem_clip.tif".format(file = demfile, data_dir = data_dir)    
   
        os.system(cmd2)

        return 0

    else:
        
        print("missing txt or dem file, can not continue. exit.")

        return 1


def analysis_via_mintpy(data_dir, projectname):
    '''
    run smallbaselineApp.py to do analysis
    '''
    os.chdir(data_dir)
    
    cmd = "smallbaselineApp.py {}/{}.cfg".format(data_dir, projectname)

    os.system(cmd)

    return



def main():

    parser = ArgumentParser()

    parser.add_argument('--gfilelist', required=True)
    
    parser.add_argument('--config', required=True)

    parser.add_argument('--outdir', required=True)

    args = parser.parse_args()

    filelist = args.gfilelist

    config_file = args.config

    outdir = args.outdir

    run_job(filelist, outdir)

    config(template_file, outdir, projectname)

    prep_data_struc(outdir, config_file)

    analysis_via_mintpy(outdir, projectname)

    return


if __name__== "__main__":

    main()

