# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 16:51:20 2018

@author: cmunoz
"""
import numpy as np
import netCDF4
import gsw
import logging

import corrections.VariableSettings as VariableSettings


def data_correction(var_attrs, var_names, metadata_file, metadata_file_info, input_data_file, output_data_file, config_settings):
    # Declare dictionaries where to store corrections attributes
    cond_corr_atts = {}
    salt_corr_atts = {}
    
    with netCDF4.Dataset(metadata_file) as nc:    
        # List variables contained in metadata file
        nc_vars = nc.variables.keys()
        #load metadata from conductivity and salinity to be corrected from sensor1 
        cond_01_corr_atts = VariableSettings.import_corrected_variable_attributes(var_attrs, nc, var_names['var_to_corr'][0])
        salt_01_corr_atts = VariableSettings.import_corrected_variable_attributes(var_attrs, nc, var_names['var_to_corr'][1])
        # in case there exists sensor 2
        if metadata_file_info['platform_subtype'] == 'ctd':
            if len(var_names['var_to_corr']) >= 2:
                if var_names['var_to_corr'][2] in nc_vars:            
                    cond_02_corr_atts = VariableSettings.import_corrected_variable_attributes(var_attrs, nc, var_names['var_to_corr'][2])           
                    salt_02_corr_atts = VariableSettings.import_corrected_variable_attributes(var_attrs, nc, var_names['var_to_corr'][3])
            
            
    with netCDF4.Dataset(input_data_file) as nc:           
        #load metadata and data from sensor 1
        cond_01_atts = VariableSettings.import_original_variable_attributes(nc, var_names['var_original'][0])
        salt_01_atts = VariableSettings.import_original_variable_attributes(nc, var_names['var_original'][1])
        cond_01_data = nc.variables[var_names['var_original'][0]][:]
        temp_01_data = nc.variables[var_names['var_aux'][0]][:]
        
        cond_corr_atts['cond_01_corr_atts'] = cond_01_corr_atts
        salt_corr_atts['salt_01_corr_atts']= salt_01_corr_atts   
        
        if metadata_file_info['platform_subtype'] == 'glider':
            prof_dir_data = nc.variables[var_names['var_aux'][2]][:]
            
        # in case there exists sensor 2
        if metadata_file_info['platform_subtype'] == 'ctd':
            if len(var_names['var_to_corr']) >= 2:
                if var_names['var_to_corr'][2] in nc_vars:
                    cond_02_atts = VariableSettings.import_original_variable_attributes(nc, var_names['var_original'][2])
                    salt_02_atts = VariableSettings.import_original_variable_attributes(nc, var_names['var_original'][3])             
                    cond_02_data = nc.variables[var_names['var_original'][2]][:]
                    temp_02_data = nc.variables[var_names['var_aux'][2]][:]
            
                cond_corr_atts['cond_02_corr_atts'] = cond_02_corr_atts
                salt_corr_atts['salt_02_corr_atts'] = salt_02_corr_atts
        
        #load data from pressure sensor   
        pres_data = nc.variables[var_names['var_aux'][1]][:]  

        #APPLY CORRECTIONS
        logging.info('Exporting corrected variables to ' + output_data_file + '\n')
        #correct conductivity values
        if config_settings['multi_coeff_A'] == False:
            if 'correction_coefficient_A' in cond_01_corr_atts:
                coefficient_A = np.float64(cond_01_corr_atts['correction_coefficient_A'])
            elif 'CorrectionCoefficient_A' in cond_01_corr_atts:
                coefficient_A = np.float64(cond_01_corr_atts['CorrectionCoefficient_A'])
            cond_01_corr_data = cond_01_data * coefficient_A
            
            if metadata_file_info['platform_subtype'] == 'glider':
                cond_01_corr_data = cond_01_corr_data * 10 # convert Sm-1 to mScm-1
                cond_01_corr_atts, cond_01_corr_data = VariableSettings.fill_empty_value_with_nan(cond_01_corr_atts, cond_01_corr_data)
        
        elif config_settings['multi_coeff_A'] == True:
            coeff_A_list = config_settings['coeff_A_list']
            idx_list = config_settings['idx_list']

            cond_01_corr_data = cond_01_data.copy()
            if config_settings['prof_dir_sections'] == False:
                range_idx = len(idx_list)-1
            elif config_settings['prof_dir_sections'] == True:
                range_idx = len(idx_list)
                
            for i in range(0, range_idx):
                coefficient_A = coeff_A_list[i]
                if config_settings['prof_dir_sections'] == False:
                    cond_01_corr_data[idx_list[i]:idx_list[i+1]] = cond_01_data[idx_list[i]:idx_list[i+1]] * coefficient_A
                elif config_settings['prof_dir_sections'] == True:
                    cond_01_corr_data[prof_dir_data == idx_list[i]] = cond_01_data[prof_dir_data == idx_list[i]] * coefficient_A                    
            if metadata_file_info['platform_subtype'] == 'glider':
                cond_01_corr_data = cond_01_corr_data * 10 # convert Sm-1 to mScm-1
                cond_01_corr_atts, cond_01_corr_data = VariableSettings.fill_empty_value_with_nan(cond_01_corr_atts, cond_01_corr_data)
        
                
        #derive corrected salinities using gsw package
        salt_01_corr_data = gsw.SP_from_C(cond_01_corr_data,temp_01_data,pres_data)
        if metadata_file_info['platform_subtype'] == 'glider':
            salt_01_corr_atts, salt_01_corr_data = VariableSettings.fill_empty_value_with_nan(salt_01_corr_atts, salt_01_corr_data)
        
            
        # in case there exists sensor 2
        if metadata_file_info['platform_subtype'] == 'ctd':
            if len(var_names['var_to_corr']) >= 2:
                if var_names['var_to_corr'][2] in nc_vars:
                    if 'correction_coefficient_B' in cond_02_corr_atts:
                        coefficient_B = cond_02_corr_atts['correction_coefficient_B']
                    elif 'CorrectionCoefficient_B' in cond_02_corr_atts:
                        coefficient_B = cond_02_corr_atts['CorrectionCoefficient_B']
                    cond_02_corr_data = cond_02_data * coefficient_B
                    #cond_02_corr_atts, cond_02_corr_data = VariableSettings.fill_empty_value_with_nan(cond_02_corr_atts, cond_02_corr_data)
                    #derive corrected salinities using gsw package
                    salt_02_corr_data = gsw.SP_from_C(cond_02_corr_data,temp_02_data,pres_data)
                    #salt_02_corr_atts, salt_02_corr_data = VariableSettings.fill_empty_value_with_nan(salt_02_corr_atts, salt_02_corr_data)      

            
        #WRITE CORRECTED VARIABLES
        #write conductivity and salinity corrected variables corrected L1 file
        with netCDF4.Dataset(output_data_file, 'r+') as nc:  
            #generate corrected variables to fill data&metadata
            VariableSettings.create_corrected_variable(metadata_file_info, nc, var_names['var_to_corr'][0],cond_01_corr_data,cond_01_atts,cond_01_corr_atts) 
            VariableSettings.create_corrected_variable(metadata_file_info, nc, var_names['var_to_corr'][1],salt_01_corr_data,salt_01_atts,salt_01_corr_atts)
            # in case there exists sensor 2
            if metadata_file_info['platform_subtype'] == 'ctd':
                if len(var_names['var_to_corr']) >= 2:
                    if var_names['var_to_corr'][2] in nc_vars:
                        VariableSettings.create_corrected_variable(metadata_file_info,nc, var_names['var_to_corr'][2],cond_02_corr_data,cond_02_atts,cond_02_corr_atts)
                        VariableSettings.create_corrected_variable(metadata_file_info,nc, var_names['var_to_corr'][3],salt_02_corr_data,salt_02_atts,salt_02_corr_atts)
    
        # Edit global attributes
        with netCDF4.Dataset(output_data_file, 'r+') as nc: 
            nc.setncattr('data_mode', 'DM')
            nc.setncattr('processing_level', 'L1_corr processed data with salinity and conductivity corrections')
            nc.setncattr('history', 'Product generated by the glider toolbox version 1.3.0 (https://github.com/socib/glider_toolbox). Salinity and conductivity corrections generated by the SOCIB Salinity Correction Toolbox version 0.1.0')
        return cond_corr_atts, salt_corr_atts
        
        