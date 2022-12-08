#!/usr/bin/env python3

'''
'''
import os
import sys
import h5py
import regex as re
import numpy as np


import utils




SLURM_ID = int(sys.argv[1])



run_ids, cryst_delay_ts = utils.read_exp_params()


run_id = run_ids[SLURM_ID]
cryst_delay_t = cryst_delay_ts[SLURM_ID]




concat_file = utils.concat_file(f'{utils.CRYSTFEL_DIR}/{run_id}/{utils.CRYSTFEL_GRP}/crystfel.total')

detx = utils.grep(concat_file, r'(?<=det_shift x \= )[-]?\d*.\d*', float)
dety = utils.grep(concat_file, r'(?<=det_shift.* y \= )[-]?\d*.\d*', float)







h5fname = f'detxy-{utils.CRYSTFEL_GRP}-run{run_id}'

if os.path.exists(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5'):
    os.remove(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5')

with h5py.File(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5', 'a') as h5file:
    h5file[f'/detx'] = np.array(detx)
    h5file[f'/dety'] = np.array(dety)




