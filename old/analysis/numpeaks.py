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


numpeaks = utils.grep(concat_file, r'(?<=num_peaks \= )\d+', int)




h5fname = f'numpeaks-{utils.CRYSTFEL_GRP}-run{run_id}'




if os.path.exists(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5'):
    os.remove(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5')

with h5py.File(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5', 'a') as h5file:

    h5file[f'/numpeaks'] = np.array(numpeaks)



