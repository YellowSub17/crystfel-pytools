#!/bin/bash


##### srun --partition=all --ntasks=35 ./srun_peakxy.sh

python peakxy.py $SLURM_PROCID

exit
