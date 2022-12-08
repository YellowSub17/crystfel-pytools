#!/bin/bash


##### srun --partition=all --ntasks=35 ./srun_unitcells.sh

python unitcells.py $SLURM_PROCID

exit
