



import os
import glob
import h5py
import numpy as np



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

    def mk_mask(self,):

        print(f'Making mask.')

        lst_file = open(f'{self.prjdir}/{self.grpname}files.lst', 'r')
        lst_file_lines =  lst_file.read().split('\n')[:-1]
        lst_file.close()


        lst_files = list(set(map(lambda x: x.split(' //')[0], lst_file_lines)))
        print(lst_files)


        with h5py.File(lst_files[0], 'r') as f:
            _, eigernx, eigerny = f['/entry/data/data'].shape

        run_sum = np.zeros( (eigernx, eigerny) )
        run_sumsq = np.zeros((eigernx, eigerny))

 
        print(f'Summing {len(lst_file_lines)} frames.')
        for lst_file_num, lst_file in enumerate(lst_files[:10]):
            print(f'{lst_file_num}/{len(lst_files)}', end='\r')

            with h5py.File(lst_file, 'r') as f:
                d = f['/entry/data/data'][:]

            run_sum+=np.sum(d, axis=0)
            run_sumsq+=np.sum(d**2, axis=0)



        run_mean = run_sum/len(lst_files[:10])
        run_std = np.sqrt(np.abs(run_sumsq/len(lst_files[:10]) - run_mean**2))


#location where mean is high and where std is nan is where we want to mask
# for some reason hot pixels give div 0 error
        loc1 = np.where(run_mean>20)
        # loc2 = np.where(np.isnan(run_std))

# make mask
        mask = np.zeros((eigernx, eigerny))
        mask[loc1]=1
        # mask[loc2]=1


# save mask
        h5file = h5py.File(f'{self.prjdir}/{self.grpname}mask.h5', 'w')
        h5file['/mask'] = mask
        h5file['/sum'] = run_sum
        h5file['/sumsq'] = run_sumsq
        h5file['/mean'] = run_mean
        h5file['/std'] = run_std

        h5file.close()









        

        
        
        



if __name__=='__main__':

    cj = CrystProj(
        datadir = '/beegfs/desy/user/patricka/mx2/data',
        grpname = '0095',
        workdir = '/beegfs/desy/user/patricka/mx2/crystfel_calc'
    )

    # cj.mk_proj_dir()
    cj.mk_lst(f'*_{cj.grpname}_data*', overwrite=True)
    cj.mk_mask()





















