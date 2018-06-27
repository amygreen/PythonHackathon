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
        self.calculate_zscore()
        self.calculate_atlas_zscores()

    def load_data(self):
        self.subject_img = nib.load(self.subject_nii_path)
        self.mean_img = nib.load(self.mean_nii_path)
        self.sd_img = nib.load(self.sd_nii_path)
        self.atlas_img = nib.load(self.atlas_nii_path)

        self.subject_data = self.subject_img.get_data()
        self.mean_data = self.mean_img.get_data()
        self.sd_data = self.sd_img.get_data()
        self.atlas_data = self.atlas_img.get_data()

        self.subject_data[self.subject_data==0] = np.nan
        self.mean_data[self.mean_data == 0] = np.nan
        self.sd_data[self.sd_data == 0] = np.nan


    def calculate_zscore(self):
        self.zscores = (self.subject_data - self.mean_data) / self.sd_data

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
