#!/bin/bash


##### srun --partition=all --ntasks=35 ./srun_numpeaks.sh

python numpeaks.py $SLURM_PROCID

exit
