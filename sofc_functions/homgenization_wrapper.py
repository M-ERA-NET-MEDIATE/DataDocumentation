# -*- coding: utf-8 -*-
"""
Wrapper functions for the generation of the SOFC parameters
"""
from datetime import datetime
from dlite import Instance
from pathlib import Path
import pandas as pd


"""
List of instances that are required:

   - RVE_generation_input:      http://onto-ns.com/meta/0.1/SOFC_RVE_generation
   - RVE represented as voxel:  http://onto-ns.com/meta/0.1/VoxelImageBW
   - Meshing parameters:        http://onto-ns.com/meta/0.1/SOFC_RVE_meshing
   - Mesh:                      http://onto-ns.com/meta/0.1/HexadralMesh3D
   - RVE properties             http://onto-ns.com/meta/0.1/SOFC_RVE_properties
   - homogenization results (equivalent to RVE properties?)
   - averaged homogenization results (equivalent to RVE properties?)
   - properties for COMSOL (restriction of RVE properties?)
"""


def wrapper_RVE_generation(inputRVE:Instance,label:str):
    """
    Function to create the RVE domain and return them as DLite Instance

    Input:
        - inputRVE: parameters for the generation of the RVE
            provided as a DLite Instance of http://onto-ns.com/meta/0.1/SOFC_RVE_generation

    Return:
        - rveOut: dlite.Instance of type http://onto-ns.com/meta/0.1/VoxelImageBW
    """
    # convert to the expected format
    params = get_rve_parameters(inputRVE=inputRVE)

    # create the values
    voxels = create_RVE(params=params)

    # convert to expected format
    generatedParameters = get_rve_instance(voxels,label=label)

    return generatedParameters


#-------------------------------------------------------------------------
# core functions
#-------------------------------------------------------------------------

def create_RVE(params:dict):
    """
    Fake function to represent the RVE generation submodule
    """