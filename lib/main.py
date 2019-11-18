# -*- coding: utf-8 -*-
"""

Created on Thu Aug  9 14:11:42 2018

@author: cmunoz
"""
import sys
import os
import utils.SetPaths as SetPaths
import utils.ListFiles as ListFiles
import utils.FileSettings as FileSettings

import corrections.CorrectionsManager as CorrectionsManager
import corrections.DbCorrectionsManager as DbCorrectionsManager
import config.config as config


input_data_path = sys.argv[1]
#input_data_path = '/LOCALDATA/MATLAB/salinity-correction-toolbox/lib/ctd-salinity-correction-pack/out/prod/data/correction_data/correction_coefficients/correction_coefficients_nc/'

# Import Configuration parameters
config_settings = config.load_config(input_data_path)

# Set paths
main_path = SetPaths.set_main_path(config_settings)
metadata_input_files_path = SetPaths.set_input_metadata_path(config_settings, main_path)
metadata_input_files_list = ListFiles.list_input_files(metadata_input_files_path)

for i in range(0,len(metadata_input_files_list)):
    
    metadata_file = metadata_input_files_list[i]
    
    # Obtain file information
    metadata_file_info = FileSettings.get_metadata_filename_info(metadata_file, config_settings)
    
    # Set output path
    data_input_file_path, data_input_filename = SetPaths.set_input_data_path(config_settings['test_mode'], main_path, metadata_file_info)
    data_output_file_path, data_output_filename = SetPaths.set_output_data_path(config_settings['test_mode'], main_path, metadata_file_info)
    
    # Copy file L1 and rename with L1_corr
    FileSettings.copy_input_data_file(data_input_file_path, data_input_filename, data_output_file_path, data_output_filename)
    input_data_file = data_input_file_path + data_input_filename[0]
    output_data_file = data_output_file_path + data_output_filename[0]
    
    # Load variables, apply corrections and write corrections to L1_corr file
    if metadata_file_info['platform_subtype'] == 'ctd':
        var_names = config_settings['ctd_variables']



    elif metadata_file_info['platform_subtype'] == 'glider':
        var_names = config_settings['glider_variables']
    
    # Load variable attributes list from configuration parameters    
    var_attrs = config_settings['var_attrs']
    
    # Run corrections Manager
    cond_corr_atts, salt_corr_atts = CorrectionsManager.data_correction(var_attrs, var_names, metadata_file, metadata_file_info, input_data_file, output_data_file, config_settings)    
    
    # Export corrections to database
    DbCorrectionsManager.export_corrections_to_db( cond_corr_atts, salt_corr_atts, metadata_file_info )
    

        