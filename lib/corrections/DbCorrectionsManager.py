# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 06:52:30 2018

@author: cmunoz
"""
import utils.db_connect as db_connect
from datetime import datetime
import pandas as pd


def export_corrections_to_db( cond_corr_atts, salt_corr_atts, metadata_file_info ):   
    ## Read deployment_name from database
    query = ['SELECT deployment_id FROM instrumentation.deployment WHERE deployment_code = ' + 
    '\'' + metadata_file_info['deployment_code'][3:7] + '\'' + 
    ' AND deployment_instrument_id = (SELECT instrument_id FROM instrumentation.instrument WHERE instrument_name = ' + 
    '\''+ metadata_file_info['instrument_name'].upper() + '\'' + ');']
    cursor, conn = db_connect.connect_db()
    deployment_id = db_connect.query_db(cursor, conn, query[0])
    #convert to integer
    deployment_id = list(deployment_id[0])
    deployment_id = deployment_id[0]
    deployment_id = int(deployment_id)
    
    user_id = 1
    
    ## Check existing corrections done in database  
    if metadata_file_info['platform_subtype'] == 'ctd':         
        query = 'SELECT ctd_salinity_correction_deployment_id FROM corrections.ctd_salinity_correction;'
    
    elif metadata_file_info['platform_subtype'] == 'glider':
        query = 'SELECT glider_salinity_correction_deployment_id FROM corrections.glider_salinity_correction;'
    
    cursor, conn = db_connect.connect_db()
    deployment_id_query = db_connect.query_db(cursor, conn, query)
    deployment_id_list = pd.DataFrame(deployment_id_query, columns=['deployment_id'])
    
    ## CTD    
    if metadata_file_info['platform_subtype'] == 'ctd':        
        ## Write correction metadata into database     
        arguments = {'int1': deployment_id, 
                     'float1': cond_corr_atts['cond_01_corr_atts']['correction_coefficient_A'],
#                     'float1': cond_corr_atts['cond_01_corr_atts'][list(cond_corr_atts['cond_01_corr_atts'])[2]], # correction coefficient
                     'float2': salt_corr_atts['salt_01_corr_atts'][list(salt_corr_atts['salt_01_corr_atts'])[2]], # mean residual salinity differences
                     'float3': salt_corr_atts['salt_01_corr_atts'][list(salt_corr_atts['salt_01_corr_atts'])[4]], # std residual salinity differences
                     'date1':datetime.now().date().strftime('%Y-%m-%d'),
                     'int2': user_id,
                     'date2':datetime.now().date().strftime('%Y-%m-%d'),
                     'int3': user_id}
        if len(cond_corr_atts) == 2:
            arguments['float4'] = cond_corr_atts['cond_02_corr_atts']['correction_coefficient_B']
            arguments['float5'] = salt_corr_atts['salt_02_corr_atts']['residual_salinity_differences_mean']
            arguments['float6'] = salt_corr_atts['salt_02_corr_atts']['residual_salinity_differences_std']
            
        if deployment_id in deployment_id_list.deployment_id.values:
            if len(cond_corr_atts) == 1:
                query = ['UPDATE corrections.ctd_salinity_correction SET ' + 
                    'ctd_salinity_correction_sensor_01_corr_coeff = %(float1)s, ' +
                    'ctd_salinity_correction_sensor_01_mean_resid = %(float2)s, ' +
                    'ctd_salinity_correction_sensor_01_std_resid = %(float3)s, ' +
                    'updated_on = %(date2)s, ' +
                    'updated_by_id = %(int3)s ' +
                    'WHERE ctd_salinity_correction_deployment_id = \'' + str(deployment_id) + '\';']
            elif len(cond_corr_atts) == 2:
                query = ['UPDATE corrections.ctd_salinity_correction SET ' + 
                    'ctd_salinity_correction_sensor_01_corr_coeff = %(float1)s, ' +
                    'ctd_salinity_correction_sensor_01_mean_resid = %(float2)s, ' +
                    'ctd_salinity_correction_sensor_01_std_resid = %(float3)s, ' +
                    'ctd_salinity_correction_sensor_02_corr_coeff = %(float4)s, ' +
                    'ctd_salinity_correction_sensor_02_mean_resid = %(float5)s, ' +
                    'ctd_salinity_correction_sensor_02_std_resid = %(float6)s, ' +
                    'updated_on = %(date2)s, ' +
                    'updated_by_id = %(int3)s ' +
                    'WHERE ctd_salinity_correction_deployment_id = \'' + str(deployment_id) + '\';']
        
        elif deployment_id not in deployment_id_list.deployment_id.values or deployment_id_list.empty():     
            query = ['INSERT INTO corrections.ctd_salinity_correction' +
                    '(ctd_salinity_correction_deployment_id, ctd_salinity_correction_sensor_01_corr_coeff, ctd_salinity_correction_sensor_01_mean_resid,' + 
                    'ctd_salinity_correction_sensor_01_std_resid, created_on, created_by_id, updated_on, updated_by_id)' +
                    'VALUES (%(int1)s, %(float1)s, %(float2)s, %(float3)s, %(date1)s, %(int2)s, %(date2)s, %(int3)s);']
                    
 
           
    ## Glider
    elif metadata_file_info['platform_subtype'] == 'glider':  
        # Get CTD correction deployment info
        ctd_deployment_info = salt_corr_atts['salt_01_corr_atts']['background_data_used_for_correction']        
        ctd_deployment_info = ctd_deployment_info.split('dep',1)[1]
        ctd_deployment_info = ctd_deployment_info.split('_')
        # Get CTD correction deployment id from database
        query = ['SELECT deployment_id FROM instrumentation.deployment WHERE deployment_code = ' + 
        '\'' + str(ctd_deployment_info[0]) + '\'' + 
        ' AND deployment_instrument_id = (SELECT instrument_id FROM instrumentation.instrument WHERE instrument_name = ' + 
        '\''+ str(ctd_deployment_info[2].upper()) + '\'' + ');']
        cursor, conn = db_connect.connect_db()
        ctd_deployment_id = db_connect.query_db(cursor, conn, query[0]) 
        #convert to integer
        ctd_deployment_id = list(ctd_deployment_id[0])
        ctd_deployment_id = ctd_deployment_id[0]
        ctd_deployment_id = int(ctd_deployment_id) 
        
        query = ['SELECT ctd_salinity_correction_id FROM corrections.ctd_salinity_correction WHERE ctd_salinity_correction_deployment_id = ' + 
        '\'' + str(ctd_deployment_id) + '\'' + ';']
        cursor, conn = db_connect.connect_db()
        ctd_corr_deployment_id = db_connect.query_db(cursor, conn, query[0])         
        #convert to integer
        ctd_corr_deployment_id = list(ctd_corr_deployment_id[0])
        ctd_corr_deployment_id = ctd_corr_deployment_id[0]
        ctd_corr_deployment_id = int(ctd_corr_deployment_id)
        
        ## Write correction metadata into database     
        arguments = {'int1': deployment_id, 
                     'float1': cond_corr_atts['cond_01_corr_atts']['correction_coefficient_A'], 
                     'text1': salt_corr_atts['salt_01_corr_atts']['residual_salinity_differences_std_background_data'], 
                     'float3': salt_corr_atts['salt_01_corr_atts']['salinity_error_estimate'],
                     'int2': ctd_corr_deployment_id,
                     'text2': cond_corr_atts['cond_01_corr_atts']['theta-sal_whitespace_for_correction'],
                     'date1':datetime.now().date().strftime('%Y-%m-%d'),
                     'int3': user_id,
                     'date2':datetime.now().date().strftime('%Y-%m-%d'),
                     'int4': user_id}
        
        if deployment_id in deployment_id_list.deployment_id.values:
            query = ['UPDATE corrections.glider_salinity_correction SET ' + 
                    'glider_salinity_correction_sensor_01_corr_coeff = %(float1)s, ' +
                    'glider_salinity_correction_residual_salinity_differences = %(text1)s, ' +
                    'glider_salinity_correction_salinity_error_estimate = %(float3)s, ' +
                    'glider_salinity_correction_background_data_id = %(int2)s, ' +
                    'glider_salinity_correction_theta_sal_range = %(text2)s, ' +
                    'updated_on = %(date2)s, ' +
                    'updated_by_id = %(int3)s ' +
                    'WHERE glider_salinity_correction_deployment_id = \'' + str(deployment_id) + '\';']
        
        elif deployment_id not in deployment_id_list.deployment_id.values or deployment_id_list.empty():     
            query = ['INSERT INTO corrections.glider_salinity_correction ' +
                    '(glider_salinity_correction_deployment_id, glider_salinity_correction_sensor_01_corr_coeff, glider_salinity_correction_residual_salinity_differences,' + 
                    'glider_salinity_correction_salinity_error_estimate, glider_salinity_correction_background_data_id,' + 
                    'glider_salinity_correction_theta_sal_range,' + 
                    'created_on, created_by_id, updated_on, updated_by_id) ' +
                    'VALUES (%(int1)s, %(float1)s, %(text1)s, %(float3)s, %(int2)s, %(text2)s, %(date1)s, %(int3)s, %(date2)s, %(int4)s);']
                    
                    
        #cond_corr_atts['cond_01_corr_atts']['background_data_used_for_correction']
                   
    cursor, conn = db_connect.connect_db()
    db_connect.write_db(cursor, conn, query[0], arguments) 
    
    
