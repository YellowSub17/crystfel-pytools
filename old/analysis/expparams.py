#!/usr/bin/env python3

'''
Save initial metadata for 
'''
import h5py
import numpy as np
import os






scratch_dir = '/asap3/petra3/gpfs/p11/2022/data/11014376/scratch_cc/pat/'


run_ids = []
run_ids += [i for i in range(11, 25)]
run_ids += [i for i in range(40, 53)]
run_ids += [i for i in range(53, 61)]

cryst_delay_ts = []
cryst_delay_ts += [45 , 40, 35, 30, 25, 20, 15, 10, 5, 11, 11, 13, 17, 17] # 11-24
cryst_delay_ts += [5, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 25] # 40-52
cryst_delay_ts += [40, 30, 20, 10, 40, 30, 20, 10] # 53- 60



num_frames = [100000]*len(run_ids)
num_frames[-3] = 99999
num_frames[12] = 82000

prorat = []
prorat += [1 for i in range(11, 25)]
prorat += [1 for i in range(40, 53)]
prorat += [0.75 for i in range(53, 57)]
prorat += [1.25 for i in range(57, 61)]






# grp_names = ['pk8_thr5_snr5','pk8_thr10_snr5', 'pk8_thr50_snr5', ]




if os.path.exists(f'{scratch_dir}/results/expparams.h5'):
    os.remove(f'{scratch_dir}/results/expparams.h5')

with h5py.File(f'{scratch_dir}/results/expparams.h5', 'w') as h5file:
    h5file['/run_ids'] = run_ids
    h5file['/cryst_delay_ts'] = cryst_delay_ts
    h5file['/num_frames'] = num_frames
    h5file['/prorat'] = prorat

    # h5file['/grp_names'] = grp_names




