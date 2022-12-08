#!/usr/bin/env python3

'''
'''
import os
import sys
import h5py
import regex as re
# import re
import numpy as np

import utils





run_ids, cryst_delay_ts = utils.read_exp_params()

numxtals = []
# numindexable = []

for i_run_id,  run_id in enumerate(run_ids):


    concat_file = utils.concat_file(f'{utils.CRYSTFEL_DIR}/{run_id}/{utils.CRYSTFEL_GRP}/stderr.total')

    run_xtals = utils.grep(concat_file, r'(?<=Final.*)\d+(?= crystals)' , int)
    # run_indexable = utils.grep(concat_file,r'(?<=Final.*)\d+(?= indexable)', int)

    numxtals.append(sum(run_xtals))
    # numindexable.append(sum(run_indexable))


h5fname = f'numxtals-{utils.CRYSTFEL_GRP}'

if os.path.exists(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5'):
    os.remove(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5')

with h5py.File(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5', 'a') as h5file:
    h5file[f'/numxtals'] = np.array(numxtals)


# h5fname = f'numindexable-{utils.CRYSTFEL_GRP}'

# if os.path.exists(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5'):
    # os.remove(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5')

# with h5py.File(f'{utils.SCRATCH_DIR}/results/{h5fname}.h5', 'a') as h5file:
    # h5file[f'/data/'] = np.array()



