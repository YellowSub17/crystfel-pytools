



import os
import glob




class CrystProj:



    def __init__(self, datadir, grpname, workdir):

        self.datadir = datadir
        self.grpname = grpname
        self.workdir =  workdir
        self.prjdir = f'{workdir}/{grpname}'





    def mk_proj_dir(self):
        if not os.path.exists(self.prjdir):
            os.mkdir(self.prjdir)


    def mk_lst(self, glob_term, overwrite=False):

        #get data filenames
        h5_data_files = glob.glob(f'{self.datadir}/{glob_term}')

        if (not overwrite) and os.path.exists(f'{self.prjdir}/{self.grpname}files.lst'):
            print('WARNING: lst file exists. set overwrite=True in method to overwrite.')
            return None
        #open lst file object
        lst_file = open(f'{self.prjdir}/{self.grpname}files.lst', 'w')

        #for each file
        for h5_data_file_num, h5_data_file in enumerate(h5_data_files):
            #check how many frames are in the file
            with h5py.File(h5_data_file, 'r') as f:
                n_frames, _, _ = f['/entry/data/data'].shape
            #write each frame adress to the lst file
            for frame_num in range(n_frames):
                lst_file.write(f'{h5_data_file} //{frame_num}\n')



if __name__=='__main__':

    cj = CrystProj(
        datadir = '/beegfs/desy/user/patricka/mx2/data',
        grpname = '0095',
        workdir = '/beegfs/desy/user/patricka/mx2/crystfel_calc'
    )

    cj.mk_proj_dir()
    cj.mk_lst()



















