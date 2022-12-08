#!/usr/bin/env python3

'''
'''
import os
import sys
import h5py
import numpy as np

import utils








SLURM_ID = int(sys.argv[1])

run_ids, cryst_delay_ts = utils.read_exp_params()

run_id = run_ids[SLURM_ID]



concat_file = utils.concat_file(f'{utils.CRYSTFEL_DIR}/{run_id}/{utils.CRYSTFEL_GRP}/crystfel.total')


ss = utils.grep(concat_file, r'-?\d+\.?\d*(?= panel0)', fn=float )

peakpos = utils.grep(concat_file, r'-?\d+\.?\d*(?=.*\d panel0)', fn=float )

h = peakpos[::9]
k = peakpos[1::9]
l = peakpos[2::9]
intens = peakpos[3::9]
fs = peakpos[7::9]

# I_sigma = peakpos[4::9]
# peak = peakpos[5::9]
# background = peakpos[6::9]





h5fname = f'xtalpeakpos-{utils.CRYSTFEL_GRP}-run{run_id}'

if os.path.exists(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5'):
    os.remove(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5')

with h5py.File(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5', 'a') as h5file:


    h5file[f'/h'] = np.array(h)
    h5file[f'/k'] = np.array(k)
    h5file[f'/l'] = np.array(l)
    h5file[f'/fs'] = np.array(fs)
    h5file[f'/ss'] = np.array(ss)
    h5file[f'/inten'] = np.array(intens)





