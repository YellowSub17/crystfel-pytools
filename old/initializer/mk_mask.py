#!/usr/bin/env python3

import h5py
import hdf5plugin
import sys
import numpy as np


import matplotlib.pyplot as plt


# DATAFILE = '/media/pat/datadrive/mx2tape/h5s/lyso_control1_0087_data_000170.h5'
# MASKFILE = '/home/pat/Documents/cloudstor/phd/python_projects/mx2_analysis/mask.h5'

#Any random run with hot pixels
DATAFILE = '/beegfs/desy/user/patricka/mx2/data/lyso_jinxed_alessa_1_0092_data_000001.h5'

#mask file that will be saved
MASKFILE = '/beegfs/desy/user/patricka/mx2/crystfel_calc/mask.h5'



#extract data shape
h5file_data = h5py.File(DATAFILE, 'r')
NFRAMES, EIGER_NX, EIGER_NY = h5file_data['entry/data/data'].shape
h5file_data.close()

#10 frames is enough to average over to find hot pixels
NFRAMES=10


#find sum of the frames and sum of frames^2
run_sum = np.zeros( (EIGER_NX, EIGER_NY) )
run_sumsq = np.zeros((EIGER_NX, EIGER_NY))

h5file = h5py.File(DATAFILE, 'r')
for i in range(NFRAMES):
    print(i)
    run_sum += h5file['/entry/data/data'][i,:,:]
    run_sumsq +=  h5file['/entry/data/data'][i,:,:]**2


h5file.close()


# calculate means and std
run_mean = run_sum/NFRAMES
run_std = np.sqrt(run_sumsq/NFRAMES - run_mean**2)


#location where mean is high and where std is nan is where we want to mask
# for some reason hot pixels give div 0 error
loc1 = np.where(run_mean>20)
loc2 = np.where(np.isnan(run_std))

# make mask
mask = np.zeros((EIGER_NX, EIGER_NY))
mask[loc1]=1
mask[loc2]=1


# save mask
h5file = h5py.File(MASKFILE, 'w')
h5file['/entry/data/data'] = mask
h5file.close()

















