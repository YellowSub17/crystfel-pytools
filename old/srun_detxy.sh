#!/bin/bash


##### srun --partition=all --ntasks=35 ./srun_detxy.sh

python detxy.py $SLURM_PROCID

exit
