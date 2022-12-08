#''''''''''''!/usr/bin/env python3

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


peakpos = utils.grep(concat_file,r'(?<!(-)?\d+\s+(-)?\d+\s+.*)(\d+\.\d+)(?=.*panel0)', fn=lambda x: float(x[2]))



fs = peakpos[::4]
ss = peakpos[1::4]
q = peakpos[2::4]
intens = peakpos[3::4]



h5fname = f'peakpos-{utils.CRYSTFEL_GRP}-run{run_id}'

if os.path.exists(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5'):
    os.remove(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5')

with h5py.File(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5', 'a') as h5file:


    h5file[f'/fs'] = np.array(fs)
    h5file[f'/ss'] = np.array(ss)
    h5file[f'/q'] = np.array(q)
    h5file[f'/inten'] = np.array(intens)





