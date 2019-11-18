# -*- coding: utf-8 -*-
"""
Configuration file 


Created on Thu Aug  9 16:36:06 2018
@author: cmunoz
"""
def load_config(input_data_path):
    # Set operation mode
    test_mode = True
    multi_coeff_A = False
    prof_dir_sections = False
    
    # in case multi_coeff_A is True, list coefficients and data idx ranges to be applied
    #dep0001_sdeep05_scb-sldeep005_L1_corr_2017-03-03 sections
#    coeff_A_list = [1.000452, 1.000381, 1.000441, 1.000369, 1.000432, 1.000447, 1.000430, 1.000481, 1.000410, 1.000498, 1.000561, 1.000431, 1.000389, 1.000460, 1.000530, 1.000380, 1.000601, 1.000702, 1.000782]
#    idx_list = [1, 807051, 842251, 846501,852001, 870001,930001, 947001, 956001, 972001, 1012001, 1158292, 1162501, 1185001, 1210001, 1300001, 1505001,1840001, 2550001, 2615737]
#    SOCIB_ENL_CANALES_NOV2017_SDEEP05_GFMR0065
#    coeff_A_list = [1.000339000000000, 1.000139000000000, 1.000130999999999, 1.000101000000000]
#    idx_list = [1, 245201, 376501, 615101, 772869]
#    sdeep05 may2018    
#    coeff_A_list = [0.999312, 0.999681, 0.999819]
#    idx_list = [1, 30651, 49201, 64579]
#    sdeep04 may2019
#    coeff_A_list = [1.000267, 1.000199, 1.000201]
#    idx_list = [1, -1, 0]
#    sdeep04 jul2019
#    coeff_A_list = [1.000148, 1.000001, 1.000097]
#    idx_list = [1, -1, 0]
    #    sdeep04 apr2019
#    coeff_A_list = [1.000280, 1.000178, 1.000360]
#    idx_list = [1, -1, 0]
    
    
    # LIST PLATFORM NAMES
    rv_name = ['socib-rv', 'garcia-del-cid-rv', 'alliance-rv', 'pourquoipas-rv']
    glider_name = ['sdeep00','sdeep01','sdeep02','sdeep03','sdeep04','sdeep05', 
                   'ideep00','ideep01','ideep02','icoast00']
       
    # DECLARE CTD VARIABLES
    var_original = ['COND_01', 'SALT_01', 'COND_02','SALT_02']
    var_aux = ['WTR_TEM_01','WTR_PRE','WTR_TEM_02']
    var_to_corr = ['COND_01_CORR', 'SALT_01_CORR', 'COND_02_CORR', 'SALT_02_CORR']
    ctd_variables = {'var_original': var_original, 'var_aux': var_aux, 'var_to_corr': var_to_corr}
    
    # DECLARE GLIDER VARIABLES
#    var_original = ['conductivity_corrected_thermal', 'salinity_corrected_thermal']
#    var_aux = ['temperature_corrected_thermal','pressure']
    var_original = ['conductivity', 'salinity']
    var_aux = ['temperature','pressure', 'profile_direction']
    var_to_corr = ['conductivity_corr', 'salinity_corr'] 
    glider_variables = {'var_original': var_original, 'var_aux': var_aux, 'var_to_corr': var_to_corr}
    
    # DECLARE metadata from conductivity variables that need to be corrected from both sensors belonging to CTD and Glider
    var_attrs = ['observation_type', 
                 'calibration_equation','Calibration_equation',
                 'correction_coefficient_A', 'CorrectionCoefficient_A',
                 'comment', 
                 'correction_coefficient_B', 'CorrectionCoefficient_B', 
                 'residual_salinity_differences_mean', 'Residual_Salinity_differences_mean',
                 'residual_salinity_differences_std', 'Residual_Salinity_differences_std',
                 'conductivity_thermal_corr_used', 
                 'outlier_removal_summary', 'salinity_error_estimate', 
                 'summary_details', 'summary_method', 'summary_method_error_estimate', 
                 'summary_method_report', 'glider_report', 'background_data_used_for_correction', 
                 'residual_salinity_differences_std_background_data', 'theta-sal_whitespace_for_correction', 
                 '_ChunkSizes', '_FillValue']  
    
    # BUILD CONFIGURATION SETTINGS DICTIONARY
    if multi_coeff_A == False:
        config_settings = {'test_mode': test_mode, 'multi_coeff_A': multi_coeff_A, 'rv_name': rv_name, 'glider_name': glider_name, 
                       'ctd_variables': ctd_variables, 'glider_variables': glider_variables, 
                       'var_attrs': var_attrs, 'input_data_path': input_data_path}
    elif multi_coeff_A == True:
        config_settings = {'test_mode': test_mode, 'multi_coeff_A': multi_coeff_A, 'prof_dir_sections': prof_dir_sections, 'rv_name': rv_name, 'glider_name': glider_name, 
                       'ctd_variables': ctd_variables, 'glider_variables': glider_variables, 
                       'var_attrs': var_attrs, 'input_data_path': input_data_path, 'coeff_A_list': coeff_A_list, 'idx_list': idx_list}

                      
    return config_settings