# -*- coding: utf-8 -*-
"""
Wrapper functions for the generation of the SOFC parameters
"""
import numpy as np
from datetime import datetime
from dlite import Instance
from pathlib import Path
import pandas as pd


def get_design_parameters(inputParameters:Instance):
    """
    Function to get the design parameters in the expected format

    Input:
        - inputParameters: for all parameters to be defined
            provided as a DLite Instance of http://onto-ns.com/meta/0.1/SOFC_parameter_generation

    Return:
        - params: array of [ref, min , max]
    """
    # check that the instance is of the correct type

    # convert the instance to a dictionnary
    input_dict = inputParameters.asdict()

    params = []
    # convert to a list of [ref, min, max]
    for key in input_dict["properties"]:
        if "_ref" in key:
            vref = input_dict[key]
            vmin = input_dict[key[:-3]+"_min"]
            vmax = input_dict[key[:-3]+"_max"]
            params.append([vref,vmin,vmax])
    
    return inputParameters.nsnaps, params


def get_generated_parameters(inputParameters:Instance,array_params):
    """
    Function to return the generated parameters as a DLite Instance

    Input:
        - inputParameters: for all parameters to be defined
            provided as a DLite Instance of http://onto-ns.com/meta/0.1/SOFC_parameter_generation
        - array_params: array of the values of the each parameters for the snapshots

    Return:
        - generatedParameters: dlite.Instance of type http://onto-ns.com/meta/0.1/SOFC_parameter_study
    """


    return generatedParameters


def wrapper_in_design_parameters(inputParameters:Instance):
    """
    Function to create the design parameters and return them as DLite Instance

    Input:
        - inputParameters: for all parameters to be defined
            provided as a DLite Instance of http://onto-ns.com/meta/0.1/SOFC_parameter_generation

    Return:
        - generatedParameters: dlite.Instance of type http://onto-ns.com/meta/0.1/SOFC_parameter_study
    """
    # convert to the expected format
    nsnaps, params = get_design_parameters(inputParameters=inputParameters)

    # create the values
    array_params = create_snaps(NB_Snaps=nsnaps, params=params)

    # convert to expected format
    generatedParameters = get_generated_parameters(inputParameters=inputParameters,
                                                  array_params=array_params)

    return generatedParameters


def get_dataframe_generated_parameters(params:Instance):
    """
    Convert the data contained in the Instance into a DataFrame
    """
    df = pd.DataFrame()

    return df

    
def write_output_csv(generatedParameters:Instance,fileout:Path):
    """
    Write the output as csv file
    """

    df = get_dataframe_generated_parameters(generatedParameters)

    with open(fileout,'w') as f:
        f.write('% Generated from ParameterSampling.py, using Halton sequence at,' + \
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
        f.write(f'% Number of parameters,{generatedParameters.nparam}\n')
        f.write(f'% Number of cases,{generatedParameters.nsnaps}')
        
    df.to_csv(fileout,sep=";",mode="a")

    return


#-------------------------------------------------------------------------
# core functions
#-------------------------------------------------------------------------
def next_prime():
    def is_prime(num):
        "Checks if num is a prime value"
        for i in range(2,int(num**0.5)+1):
            if(num % i)==0: return False
        return True
    prime = 3
    while(1):
        if is_prime(prime):
            yield prime
        prime += 2

def vdc(n, base=2):
    vdc, denom = 0, 1
    while n:
        denom *= base
        n, remainder = divmod(n, base)
        vdc += remainder/float(denom)
    return vdc

def halton_sequence(size, dim):
    seq = []
    primeGen = next_prime()
    next(primeGen)
    for d in range(dim):
        base = next(primeGen)
        seq.append([vdc(i, base) for i in range(size)])
    return seq


def create_snaps(NB_Snaps:int, params):
    """
    creation of the snapshots using Halton sequence
    """
    
    NB_Param=len(params)
    
    # Generate random set
    Snapshot = halton_sequence(NB_Snaps,NB_Param)

    for i in range(0,NB_Snaps):
        for j in range(0,NB_Param):
            X = (params[j][2] - params[j][1])*Snapshot[j][i] + params[j][1]
            Snapshot[j][i]=X
                
    return Snapshot

#-------------------------------------------------------------------------
# END OF core functions
#-------------------------------------------------------------------------


def default_sets():
    """ get some default sets"""
    Geom_set=np.zeros((6,3), dtype=float)
    Geom_set[0][0] = 10.0e-3  #L_channel reference[m]
    Geom_set[0][1] =  5.0e-3  #L_channel min[m]
    Geom_set[0][2] = 15.0e-3  #L_channel max[m]    
    Geom_set[1][0] =  0.5e-3  #H_channel reference[m]
    Geom_set[1][1] =  0.25e-3 #H_channel min[m]
    Geom_set[1][2] =  0.75e-3 #H_channel max[m]    
    Geom_set[2][0] =  0.5e-3  #W_channel reference[m]
    Geom_set[2][1] =  0.25e-3 #W_channel min[m]
    Geom_set[2][2] =  0.75e-3 #W_channel max[m]    
    Geom_set[3][0] =  0.5e-3  #W_rib     reference[m]
    Geom_set[3][1] =  0.25e-3 #W_rib     min[m]
    Geom_set[3][2] =  0.75e-3 #W_rib     max[m]    
    Geom_set[4][0] =  1.0e-4  #H_Electrolyte reference[m]
    Geom_set[4][1] =  0.5e-4  #H_Electrolyte min[m]
    Geom_set[4][2] =  1.5e-4  #H_Electrolyte max[m]    
    Geom_set[5][0] =  1.0e-4  #H_GDE     reference[m]
    Geom_set[5][1] =  0.5e-4  #H_GDE     min[m]
    Geom_set[5][2] =  1.5e-4  #H_GDE     max[m]    
    Gde_set=np.zeros((12,3), dtype=float)
    Gde_set[0][0] =  0.4      #Por_cathode reference[au]
    Gde_set[0][1] =  0.2      #Por_cathode min[au]
    Gde_set[0][2] =  0.6      #Por_cathode max[au]    
    Gde_set[1][0] =  4.5      #Tor_cathode reference[au]
    Gde_set[1][1] =  1.5      #Tor_cathode min[au]
    Gde_set[1][2] =  7.5      #Tor_cathode max[au]    
    Gde_set[2][0] =  100.0    #Per_cathode reference[um^2]
    Gde_set[2][1] =  10.0     #Per_cathode min[um^2]
    Gde_set[2][2] =  300.0    #Per_cathode max[um^2]    
    Gde_set[3][0] =  1.0      #Spa_cathode reference[1/nm]
    Gde_set[3][1] =  0.5      #Spa_cathode min[1/nm]
    Gde_set[3][2] =  1.5      #Spa_cathode max[1/nm]    
    Gde_set[4][0] =  0.4      #Por_anode reference[au]
    Gde_set[4][1] =  0.2      #Por_anode min[au]
    Gde_set[4][2] =  0.6      #Por_anode max[au]    
    Gde_set[5][0] =  4.5      #Tor_anode reference[au]
    Gde_set[5][1] =  1.5      #Tor_anode min[au]
    Gde_set[5][2] =  7.5      #Tor_anode max[au]    
    Gde_set[6][0] =  100.0    #Per_anode reference[um^2]
    Gde_set[6][1] =  10.0     #Per_anode min[um^2]
    Gde_set[6][2] =  300.0    #Per_anode max[um^2]    
    Gde_set[7][0] =  1.0      #Spa_anode reference[1/nm]
    Gde_set[7][1] =  0.5      #Spa_anode min[1/nm]
    Gde_set[7][2] =  1.5      #Spa_anode max[1/nm]    
    Gde_set[8][0] =  1.0e+3   #Sig_Cathode reference[S/m]
    Gde_set[8][1] =  1.0e+2   #Sig_Cathode min[S/m]
    Gde_set[8][2] =  1.0e+4   #Sig_Cathode max[S/m] 
    Gde_set[9][0] =  1.0e+3   #Sig_Anode reference[S/m]
    Gde_set[9][1] =  1.0e+2   #Sig_Anode min[S/m]
    Gde_set[9][2] =  1.0e+4   #Sig_Anode max[S/m] 
    Gde_set[10][0] =  0.5      #Thc_Cathode reference[J/smK]
    Gde_set[10][1] =  1.0      #Thc_Cathode min[J/smK]
    Gde_set[10][2] =  2.0      #Thc_Cathode max[J/smK] 
    Gde_set[11][0] =  0.5      #Thc_Anode reference[J/smK]
    Gde_set[11][1] =  1.0      #Thc_Anode min[J/smK]
    Gde_set[11][2] =  2.0      #Thc_Anode max[J/smK] 
    Opr_set=np.zeros((4,3), dtype=float)
    Opr_set[0][0] =  1.0      #Prs_GDE reference[atm]
    Opr_set[0][1] =  0.9      #Prs_GDE min[atm]
    Opr_set[0][2] =  1.5      #Prs_GDE max[atm]    
    Opr_set[1][0] =  1073.2   #Tmp_GDE reference[K]
    Opr_set[1][1] =  800      #Tmp_GDE min[K]
    Opr_set[1][2] =  1200     #Tmp_GDE max[K]    
    Opr_set[2][0] =  2.0      #Prd_Anode reference[Pa]
    Opr_set[2][1] =  1.0      #Prd_Anode min[Pa]
    Opr_set[2][2] =  4.0      #Prd_Anode max[Pa]    
    Opr_set[3][0] =  6.0      #Prd_Cathode reference[Pa]
    Opr_set[3][1] =  4.5      #Prd_Cathode min[Pa]
    Opr_set[3][2] =  8.0      #Prd_Cathode max[Pa]    

    return Geom_set,Gde_set,Opr_set
