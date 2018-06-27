import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os

groupMD_file='/Users/ayam/Documents/PythonHackathon/Data/HealthyControls/groupMD_m.nii.gz'

class GroupStatistics():
    """
    This class gets a 4d nifti file which contains maps for a group of subjects.
    It can calculate mean and std across subjects per voxel and generates a relavant nifti map.
    """

    def __init__(self,group_file_name):
        self.groupMD_file=group_file_name
        self.groupMD_img=nib.load(self.groupMD_file)
        self.data_all_subjects = self.groupMD_img.get_data()

    def calculate_mean(self):
        self.data_mean = np.mean(self.data_all_subjects,axis=3)
        self.data_mean_img = nib.Nifti1Image(self.data_mean, np.eye(4))
        nib.save(self.data_mean_img, 'data_mean.nii.gz')

    def calculate_std(self):
        self.data_std = np.std(self.data_all_subjects,axis=3)
        self.data_std_img = nib.Nifti1Image(self.data_std, np.eye(4))
        nib.save(self.data_std_img, 'data_std.nii.gz')

#TODO check the results and make sure it does a correct mean and std per voxel,
#we checked the prepared maps and it looks different.

a=GroupStatistics(groupMD_file)
a.calculate_mean()
a.calculate_std()

