#!/bin/bash


##### srun --partition=all --ntasks=35 ./srun_xtalpeakxy.sh

python xtalpeakxy.py $SLURM_PROCID

exit
