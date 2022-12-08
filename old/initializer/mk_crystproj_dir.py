#!/usr/bin/env python3


import os

import glob

import sys
import shutil
import h5py



#dir where data is saved
DATADIR= '/beegfs/desy/user/patricka/mx2/data'

#dir to save crystfel project
CRYSTFELDIR= '/beegfs/desy/user/patricka/mx2/crystfel_calc'


RUNID = sys.argv[1]


#make run dir to save data
if not os.path.exists(f'{CRYSTFELDIR}/{RUNID}'):
    os.mkdir(f'{CRYSTFELDIR}/{RUNID}')

#copy default files to the run directoy
shutil.copy(f'./crystfel.project.default', f'{CRYSTFELDIR}/{RUNID}/crystfel.project')
shutil.copy(f'./193l.pdb', f'{CRYSTFELDIR}/{RUNID}/193l.pdb')
shutil.copy(f'./mx2eiger.geom', f'{CRYSTFELDIR}/{RUNID}/mx2eiger.geom')

# assuming ./make_mask.py has run, copy mask file to run directory
shutil.copy(f'{CRYSTFELDIR}/mx2mask.h5', f'{CRYSTFELDIR}/{RUNID}/mx2mask.h5')



####MAKE LST FILE
#get data filenames
glob_term = f'{DATADIR}/*_{RUNID}_data*.h5'
h5_data_files = glob.glob(glob_term)
print(f'Creating lst file')
print(f'Found {len(h5_data_files)} data h5s in {glob_term}')



#open lst file object
lst_file = open(f'{CRYSTFELDIR}/{RUNID}/{RUNID}files.lst', 'w')


#for each file
for h5_data_file_num, h5_data_file in enumerate(h5_data_files):
    print(f'{h5_data_file_num}', end='\r')

    #check how many frames are in the file
    with h5py.File(h5_data_file, 'r') as f:
        n_frames, _, _ = f['/entry/data/data'].shape
    #write each frame adress to the lst file
    for frame_num in range(200):
        lst_file.write(f'{h5_data_file} //{frame_num}\n')





####append lst to crystfel.project
print('\nAppending lst file to crystfel.project')
os.system(f'cat {CRYSTFELDIR}/{RUNID}/{RUNID}files.lst >> {CRYSTFELDIR}/{RUNID}/crystfel.project')























