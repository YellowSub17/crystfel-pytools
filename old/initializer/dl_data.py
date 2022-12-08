#!/usr/bin/env python3
import os


EMAIL='s3826109@student.rmit.edu.au'


DATADIR='/data/mx/19754a/frames/riboldia/d'
SAVEDIR='/beegfs/desy/user/patricka/mx2/data'

FILENAME='lyso_jinxed_alessa_2_2mm*.h5'

cmd = f'echo rsync -rtzP {EMAIL}@sftp.synchrotron.org.au:{DATADIR}/{FILENAME} {SAVEDIR}'


os.system(cmd)
