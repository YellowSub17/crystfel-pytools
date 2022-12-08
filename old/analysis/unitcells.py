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


cellparams = utils.grep(concat_file,r'(?<=Cell parameters .*)(\d+.\d+)', float)




a_lengths = cellparams[::6]
b_lengths = cellparams[1::6]
c_lengths = cellparams[2::6]
alpha_angles = cellparams[3::6]
beta_angles = cellparams[4::6]
gamma_angles = cellparams[5::6]



h5fname = f'unitcells-{utils.CRYSTFEL_GRP}-run{run_id}'

if os.path.exists(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5'):
    os.remove(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5')

with h5py.File(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5', 'a') as h5file:

    # h5file['/data/'] = np.array( [a_lengths, b_lengths, c_lengths, alpha_angles, beta_angles, gamma_angles] )

    h5file[f'/a'] = np.array(a_lengths)
    h5file[f'/b'] = np.array(b_lengths)
    h5file[f'/c'] = np.array(c_lengths)
    h5file[f'/alpha'] = np.array(alpha_angles)
    h5file[f'/beta'] = np.array(beta_angles)
    h5file[f'/gamma'] = np.array(gamma_angles)





