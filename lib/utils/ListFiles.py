# -*- coding: utf-8 -*-
"""
List all files in inputPath

Created on Thu Aug  9 16:52:19 2018
@author: cmunoz
"""
import os 
import glob

def list_input_files(metadata_input_files_path):
    metadata_input_files_list = []
    os.chdir(metadata_input_files_path) 
    for file in glob.glob("*.nc"):
        metadata_input_files_list.append(file)  
    return metadata_input_files_list