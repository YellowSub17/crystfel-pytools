
; Example geometry file for Eiger 16M detector, using its native file format
; and binning 2.

; Camera length (in m) and photon energy (eV)

clen = 0.27

photon_energy = 13000

; adu_per_photon needs a relatively recent CrystFEL version.  If your version is
; older, change it to adu_per_eV and set it to one over the photon energy in eV
adu_per_photon = 1
res = 13333.3   ; 75 micron pixel size

; These lines describe the data layout for the Eiger native multi-event files
dim0 = %
dim1 = ss
dim2 = fs
data = /entry/data/data



; Uncomment these lines if you have a separate bad pixel map (recommended!)
mask0_file = ./mx2mask.h5
mask0_data = /entry/data/data
mask0_goodbits = 0
mask0_badbits = 1




rigid_group_d0 = panel0
rigid_group_collection_det = d0

; corner_{x,y} set the position of the corner of the detector (in pixels)
; relative to the beam

panel0/min_fs = 0 
panel0/min_ss = 0
panel0/max_fs = 4149
panel0/max_ss = 4370

panel0/corner_x = -2087.46
panel0/corner_y = -2230.03
;panel0/corner_x = -2130.346392
;panel0/corner_y = -2184.369105

panel0/fs = +1.000000x +0.000000y 
panel0/ss = +0.000000x +1.000000y
panel0/coffset = 0

