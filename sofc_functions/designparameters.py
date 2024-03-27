# -*- coding: utf-8 -*-
"""
Wrapper functions for the generation of the SOFC parameters
"""
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
            vref = input_dict["properties"][key]
            vmin = input_dict["properties"][key[:-4]+"_min"]
            vmax = input_dict["properties"][key[:-4]+"_max"]
            params.append([vref,vmin,vmax])
    
    return inputParameters.nsnaps, params


def get_generated_parameters(inputParameters:Instance,array_params,label:str):
    """
    Function to return the generated parameters as a DLite Instance

    Input:
        - inputParameters: for all parameters to be defined
            provided as a DLite Instance of http://onto-ns.com/meta/0.1/SOFC_parameter_generation
        - array_params: array of the values of the each parameters for the snapshots

    Return:
        - generatedParameters: dlite.Instance of type http://onto-ns.com/meta/0.1/SOFC_parameter_study
    """
    # namespace
    ns = 'http://onto-ns.com/meta/0.1/SOFC_parameter_study'

    generatedParameters = Instance.from_metaid(ns,dims={"nsnaps":inputParameters.nsnaps})

    generatedParameters.label = label
    generatedParameters.generator = "Python function create_snaps"
    generatedParameters.method = "Halton sequence"
    generatedParameters.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # convert the instance to a dictionnary
    input_dict = inputParameters.asdict()

    iparam = 0
    for key in input_dict["properties"]:
        if key != "nsnaps":
            if "_ref" in key:
                generatedParameters[key[:-4]] = array_params[iparam]
                iparam +=1

    generatedParameters.nparam = iparam

    return generatedParameters


def wrapper_in_design_parameters(inputParameters:Instance,label:str):
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
                                                  array_params=array_params,
                                                  label=label)

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
        f.write('% Generated from '+generatedParameters.generator+
                ', using '+generatedParameters.method+' at, ' + 
                generatedParameters.date + '\n')
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
