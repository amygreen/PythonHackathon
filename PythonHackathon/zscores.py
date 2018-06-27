import numpy as np
import pandas as pd
import nibabel as nib

class SubjectAnalyzer:

    def __init__(self,subject_nii_path,mean_nii_path,sd_nii_path,atlas_nii_path):

        '''Get paths for files'''
        self.subject_nii_path = subject_nii_path
        self.mean_nii_path = mean_nii_path
        self.sd_nii_path = sd_nii_path
        self.atlas_nii_path = atlas_nii_path

        self.load_data()
        if self.is_data_proper:
            self.calculate_zscore()
            self.calculate_atlas_zscores()
        else:
            self.error_message = \
                "The following inputs: {}{}{} have an inconsistent have a dimension mismatch with the subject"
            self.error_message.format('mean map, ' if self.is_mean_proper else '',
                'st. dev. map, ' if self.is_sd_proper else '',
                'atlas, ' if self.is_atlas_proper else '')

    def load_data(self):
        self.subject_img = nib.load(self.subject_nii_path)
        self.mean_img = nib.load(self.mean_nii_path)
        self.sd_img = nib.load(self.sd_nii_path)
        self.atlas_img = nib.load(self.atlas_nii_path)

        self.shape = self.subject_img.shape
        self.is_mean_proper = self.mean_img.shape == self.shape
        self.is_sd_proper = self.sd_img.shape == self.shape
        self.is_atlas_proper = self.atlas_img.shape == self.shape

        self.is_data_proper = self.is_mean_proper and self.is_sd_proper and self.is_atlas_proper

        self.subject_data = self.subject_img.get_data()
        self.mean_data = self.mean_img.get_data()
        self.sd_data = self.sd_img.get_data()
        self.atlas_data = self.atlas_img.get_data()

        self.subject_data[self.subject_data==0] = np.nan
        self.mean_data[self.mean_data == 0] = np.nan
        self.sd_data[self.sd_data == 0] = np.nan


    def calculate_zscore(self):
        self.zscores = (self.subject_data - self.mean_data) / self.sd_data
        zscores = self.zscores
        zscores[np.isnan(zscores)] = 0
        self.significant_zscores = np.where(np.abs(zscores)<=1.96,np.nan,zscores)

    def calculate_atlas_zscores(self):
        md = np.zeros(self.atlas_data.max())
        zs = np.zeros(self.atlas_data.max())
        for i in range(1,self.atlas_data.max()+1):
            md[i-1] = np.nanmean(self.subject_data[self.atlas_data == i])
            zs[i-1] = np.nanmean(self.zscores[self.atlas_data == i])

        md_s = pd.Series(md,index = np.arange(1,self.atlas_data.max()+1))
        zs_s = pd.Series(zs,index = np.arange(1,self.atlas_data.max()+1))
        self.area_data = pd.DataFrame({'MD': md_s, 'Z-scores': zs_s})
        self.area_data.index.name = 'Area'
