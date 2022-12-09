



import os
import glob
import h5py
import numpy as np
import random



class CrystProj:



    def __init__(self, datadir, grpname, workdir, geompath=None, maskpath=None, cellpath=None):

        self.datadir = datadir
        self.grpname = grpname
        self.workdir =  workdir
        self.prjdir = f'{self.workdir}/{self.grpname}'


        if geompath is None:
            geompath=f'{self.workdir}/eiger.geom'

        if maskpath is None:
            maskpath=f'{self.workdir}/mask.h5'

        if cellpath is None:
            cellpath=f'{self.workdir}/193l.pdb'

        self.geompath = geompath
        self.maskpath = maskpath
        self.cellpath = cellpath





    def mk_proj_dir(self):
        if not os.path.exists(self.prjdir):
            os.mkdir(self.prjdir)


    def mk_lst(self, glob_term, overwrite=False):
        print(f'Making lst file.')

        #get data filenames
        h5_data_files = glob.glob(f'{self.datadir}/{glob_term}')
        print(f'Found {len(h5_data_files)} data files.')

        if (not overwrite) and os.path.exists(f'{self.prjdir}/{self.grpname}files.lst'):
            print('WARNING: lst file exists. set overwrite=True in method to overwrite.')
            return None
        #open lst file object
        lst_file = open(f'{self.prjdir}/{self.grpname}files.lst', 'w')

        #for each file
        for h5_data_file_num, h5_data_file in enumerate(h5_data_files):
            print(f'{h5_data_file_num}/{len(h5_data_files)}', end='\r')
            #check how many frames are in the file
            with h5py.File(h5_data_file, 'r') as f:
                n_frames, _, _ = f['/entry/data/data'].shape
            #write each frame adress to the lst file
            for frame_num in range(n_frames):
                lst_file.write(f'{h5_data_file} //{frame_num}\n')
        print()

    def mk_mask(self, nframes=10):

        print(f'Making mask.')

        lst_file = open(f'{self.prjdir}/{self.grpname}files.lst', 'r')
        lst_file_lines =  lst_file.read().split('\n')[:-1]
        lst_file.close()
        random.shuffle(lst_file_lines)

        if nframes <0:
            nframes=len(lst_file_lines)


        with h5py.File(lst_file_lines[0].split(' //')[0], 'r') as f:
            _, eigernx, eigerny = f['/entry/data/data'].shape

        run_sum = np.zeros( (eigernx, eigerny) )
        run_sumsq = np.zeros((eigernx, eigerny))

 
        print(f'Summing {nframes} frames.')
        for lst_file_line_num, lst_file_line in enumerate(lst_file_lines[:nframes]):
            print(f'{lst_file_line_num+1}/{nframes}', end='\r')
            lst_file, lst_frame = lst_file_line.split(' //')

            with h5py.File(lst_file, 'r') as f:
                d = f['/entry/data/data'][int(lst_frame),:,:]

            run_sum+=d
            run_sumsq+=d**2
        print()



        run_mean = run_sum/len(lst_file_lines[:nframes])
        run_std = np.sqrt(np.abs(run_sumsq/len(lst_file_lines[:nframes]) - run_mean**2))


#location where mean is high and where std is nan is where we want to mask
# for some reason hot pixels give div 0 error
        loc1 = np.where(run_mean>20)
        # loc2 = np.where(np.isnan(run_std))

# make mask
        mask = np.zeros((eigernx, eigerny))
        mask[loc1]=1
        # mask[loc2]=1


# save mask
        h5file = h5py.File(f'{self.maskpath}', 'w')
        h5file['/mask'] = mask
        h5file['/sum'] = run_sum
        h5file['/sumsq'] = run_sumsq
        h5file['/mean'] = run_mean
        h5file['/std'] = run_std
        h5file['/nframes'] = nframes

        h5file.close()



    def make_crystfel_project_file(self):
        from writers import writer_crystfel_project

        s = writer_crystfel_project(self.geompath,
                                3, 3.5, 3, self.cellpath, 'test', 'test_merge')
        
        f = open(f'{self.prjdir}/crystfel.project', 'w')
        f.write(s)
        f.close()

        

        os.system(f'cat {self.prjdir}/{self.grpname}files.lst >> {self.prjdir}/crystfel.project')

















if __name__=='__main__':

    cj = CrystProj(
        datadir = '/beegfs/desy/user/patricka/mx2/data',
        grpname = '0095',
        workdir = '/beegfs/desy/user/patricka/mx2/crystfel_calc'
    )

    cj.mk_proj_dir()
    cj.mk_lst(f'*_{cj.grpname}_data*', overwrite=True)
    cj.mk_mask(nframes=10)
    cj.make_crystfel_project_file()





















