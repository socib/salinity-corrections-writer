# -*- coding: utf-8 -*-
"""
Get file information

Created on Thu Aug  9 16:38:39 2018
@author: cmunoz
"""
import os
from shutil import copyfile


def get_metadata_filename_info(filename, config_settings):
    
    deployment_code, platform_name, instrument_name, deployment_date = filename.split('_')
    
    if platform_name in config_settings['rv_name']:
        platform_type = 'research_vessel'
        platform_subtype = 'ctd'
    elif platform_name in config_settings['glider_name']:
        platform_type = 'auv' 
        platform_subtype = 'glider'
    
    metadata_file_info = {'deployment_code': deployment_code, 
                          'platform_name': platform_name, 
                          'instrument_name': instrument_name, 
                          'deployment_date': deployment_date,
                          'platform_type': platform_type,
                          'platform_subtype': platform_subtype}
                          
    return metadata_file_info


def copy_input_data_file(data_input_file_path, data_input_filename, data_output_file_path, data_output_filename):
    
    if os.path.exists(data_output_file_path) == False:
        os.mkdir(data_output_file_path)
        
    src = data_input_file_path + data_input_filename[0]
    dst = data_output_file_path + data_output_filename[0]
    copyfile(src,dst)