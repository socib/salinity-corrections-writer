# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 11:45:48 2017

@author: cmunoz
"""
import numpy as np

def import_corrected_variable_attributes(var_attrs_list, nc_dataset, var_to_corr): 
#    #load metadata from conductivity variables that need to be corrected from both sensors
#    var_attrs_list = ['observation_type', 'Calibration_equation', 'CorrectionCoefficient_A', 'comment',
#                'CorrectionCoefficient_B', 'Residual_Salinity_differences_mean', 'Residual_Salinity_differences_std', 
#                'conductivity_Thermal_CORR_used', 'Calibration_Equation', 'outlier_removal_summary', 
#                'Salinity_error_estimate', 'Summary_details', 'Summary_Method', 'Summary_Method_error_estimate', 
#                'Summary_Method_Report', 'GLIDER_Report', 'Background_data_used_for_correction', 
#                'THETA-SAL-whitespace_for_correction', '_ChunkSizes']    
    
    var_to_corr_attrs = {}    
    #only add the attributes that already are available in the variable selected
    for i in range(0, len(var_attrs_list)):
        try:
            attr = nc_dataset.variables[var_to_corr].getncattr(var_attrs_list[i])
            var_to_corr_attrs[var_attrs_list[i]] = attr
        except:
            continue
        
    return var_to_corr_attrs;


def import_original_variable_attributes(nc_dataset, var_original): 
    var_original_attrs_list = nc_dataset.variables[var_original].ncattrs()
    var_original_attrs = {}
    
    for i in range(0, len(var_original_attrs_list)):  
        attr = nc_dataset.variables[var_original].getncattr(var_original_attrs_list[i])
        var_original_attrs[var_original_attrs_list[i]] = attr
    
    return var_original_attrs

def create_corrected_variable(metadata_file_info, nc_dataset, var_to_corr, var_corr_data, var_attrs, var_corr_attrs):
    if metadata_file_info['platform_subtype'] == 'glider':
       var_to_add = nc_dataset.createVariable(var_to_corr, float, ('time') ) 
    elif metadata_file_info['platform_subtype'] == 'ctd':  
        var_to_add = nc_dataset.createVariable(var_to_corr, float, ('time', 'depth') )
        
    nc_dataset.variables[var_to_corr][:] = var_corr_data[:]
    var_attrs.update(var_corr_attrs)
    var_to_add.setncatts(var_attrs)

def fill_empty_value_with_nan(var_to_fill_metadata, var_to_fill_data):
    for item in range(0,len(var_to_fill_data)):
        if isinstance(var_to_fill_data[item], float) == False:
            var_to_fill_data[item]=np.NaN
            
    var_to_fill_metadata.update({'_FillValue': np.NaN})

    return var_to_fill_metadata, var_to_fill_data
    
#def create_conductivity_corrected_variable(netCdfDataset, varToCorr,varCorrData,varAtts,varCorrAtts):
#
#    varToAdd = netCdfDataset.createVariable(varToCorr, float, ('time', 'depth') )
#    netCdfDataset.variables[varToCorr][:] = varCorrData[:]
#    varToAdd.setncatts({'standard_name': varAtts['standard_name'],\
#                        'long_name': varAtts['long_name'],\
#                        'units': varAtts['units'],\
#                        'ancillary_variables': varAtts['ancillary_variables'],\
#                        'coordinates': varAtts['coordinates'],\
#                        'original_units': varAtts['original_units'],\
#                        'observation_type': varAtts['observation_type'],\
#                        'original_units': varAtts['original_units'],\
#                        'observation_type': varCorrAtts['observation_type'],\
#                        'precision': varAtts['precision'],\
#                        'calibration_equation': varCorrAtts['Calibration_equation'],\
#                        'comment': varCorrAtts['comment']
#                        })
#    if varToCorr == 'COND_01_CORR':
#        varToAdd.setncatts({'correction_coefficient_A': varCorrAtts['CorrectionCoefficient_A']})
#    elif varToCorr == 'COND_02_CORR':
#        varToAdd.setncatts({'correction_coefficient_B': varCorrAtts['CorrectionCoefficient_B']})
#    return;
    
#def create_salinity_corrected_variable(netCdfDataset, varToCorr,varCorrData,varAtts,varCorrAtts):
#
#    varToAdd = netCdfDataset.createVariable(varToCorr, float, ('time', 'depth') )
#    netCdfDataset.variables[varToCorr][:] = varCorrData[:]
#    varToAdd.setncatts({'standard_name': varAtts['standard_name'],\
#                        'long_name': varAtts['long_name'],\
#                        'units': varAtts['units'],\
#                        'ancillary_variables': varAtts['ancillary_variables'],\
#                        'coordinates': varAtts['coordinates'],\
#                        'original_units': varAtts['original_units'],\
#                        'observation_type': varAtts['observation_type'],\
#                        'original_units': varAtts['original_units'],\
#                        'observation_type': varCorrAtts['observation_type'],\
#                        'precision': varAtts['precision'],\
#                        'residual_salinity_differences_mean': varCorrAtts['Residual_Salinity_differences_mean'],\
#                        'residual_salinity_differences_std': varCorrAtts['Residual_Salinity_differences_std'],\
#                        'comment': varCorrAtts['comment'],\
#                        'outlier_removal_summary': varCorrAtts['outlier_removal_summary']
#                        })
#    return;