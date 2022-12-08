

import os
import sys
import h5py
import regex as re
import numpy as np





SCRATCH_DIR = '/asap3/petra3/gpfs/p11/2022/data/11014376/scratch_cc/pat/'
RESULTS_DIR = '/asap3/petra3/gpfs/p11/2022/data/11014376/scratch_cc/pat/results/'
CRYSTFEL_DIR = '/asap3/petra3/gpfs/p11/2022/data/11014376/scratch_cc/pat/crystfel_calc/'

CRYSTFEL_GRP = 'pk8_thr5_snr5'


def read_exp_params():


    with h5py.File(f'{SCRATCH_DIR}/results/expparams.h5', 'r') as h5file:
        run_ids = h5file['/run_ids'][:]
        cryst_delay_ts = h5file['/cryst_delay_ts'][:]
        # grp_names = h5file['/grp_names'].asstr()[:]

    return run_ids, cryst_delay_ts






def concat_file(f):
    # print(f'Concantenating file: {f}')
    single_file_str = ''
    with open(f, 'r') as f:
        for line in f:
            single_file_str +=line

    return single_file_str




def grep(s, reg, fn=None):
    # print(f'greping reg: {reg}')
    found = re.findall(reg, s)
    if fn is not None:
        found = list(map(fn, found))
    return found







