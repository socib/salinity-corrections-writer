# -*- coding: utf-8 -*-
"""
Set paths to input and output data directories.

Created on Thu Aug  9 16:06:40 2018
@author: cmunoz
"""


def set_main_path(config_settings):   
    if config_settings['test_mode'] == True:
        main_path = "/home/cmunoz/Desktop/"    
    elif config_settings['test_mode'] == False:
        main_path = ""  
    return main_path
        
def set_input_metadata_path(config_settings, main_path):   
    if config_settings['test_mode'] == True:
        metadata_input_files_path = config_settings['input_data_path']    
    elif config_settings['test_mode'] == False:
        metadata_input_files_path =  config_settings['input_data_path']    
    return metadata_input_files_path
    

def set_input_data_path(test_mode, main_path, metadata_file_info):   
    if test_mode == True:
        data_input_file_path = main_path + "ctd_nc_L1_thredds/"       
    elif test_mode == False:
        data_input_file_path = ['/data/current/opendap/observational/' + 
                                    metadata_file_info['platform_type'] + '/' +
                                    metadata_file_info['platform_subtype'] + '/' +
                                    metadata_file_info['platform_name'].replace("-", "_") + '-' + 
                                    metadata_file_info['instrument_name'].replace("-", "_") + '/' +
                                    'L1/' + 
                                    metadata_file_info['deployment_date'][0:4] + '/' ]
        
    if metadata_file_info['platform_subtype'] == 'glider':
        data_input_filename =  [metadata_file_info['deployment_code'] + '_' + 
                                metadata_file_info['platform_name'] + '_' + 
                                metadata_file_info['instrument_name'] + '_L1_' + 
                                metadata_file_info['deployment_date'][0:10] + '_data_dt.nc']
    else:
        data_input_filename =  [metadata_file_info['deployment_code'] + '_' + 
                                metadata_file_info['platform_name'] + '_' + 
                                metadata_file_info['instrument_name'] + '_L1_' + 
                                metadata_file_info['deployment_date']]

    return data_input_file_path, data_input_filename

def set_output_data_path(test_mode, main_path, metadata_file_info):   
    if test_mode == True:
        data_output_file_path = main_path + "test_ctd_corrected_nc/"       
    elif test_mode == False:
        data_output_file_path = ['/data/current/opendap/observational/' + 
                                    metadata_file_info['platform_type'] + '/' +
                                    metadata_file_info['platform_subtype'] + '/' +
                                    metadata_file_info['platform_name'].replace("-", "_") + '-' + 
                                    metadata_file_info['instrument_name'].replace("-", "_") + '/' +
                                    'L1_corr/' + 
                                    metadata_file_info['deployment_date'][0:4] + '/']
                                    
    if metadata_file_info['platform_subtype'] == 'glider':                               
        data_output_filename = [metadata_file_info['deployment_code'] + '_' + 
                                metadata_file_info['platform_name'] + '_' + 
                                metadata_file_info['instrument_name'] + '_L1_corr_' + 
                                metadata_file_info['deployment_date'][0:10] + '_data_dm.nc']
    else:
        data_output_filename = [metadata_file_info['deployment_code'] + '_' + 
                                metadata_file_info['platform_name'] + '_' + 
                                metadata_file_info['instrument_name'] + '_L1_corr_' + 
                                metadata_file_info['deployment_date']]
                                
    return data_output_file_path, data_output_filename
    
    
    


        
