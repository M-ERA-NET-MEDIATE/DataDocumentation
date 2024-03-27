"""
test_function for the computation of the microstructure evolution
"""
from pathlib import Path
import os
import dlite
import json

from sofc_functions.designparameters import (
    get_design_parameters,
    create_snaps,
    get_generated_parameters,
)

root = Path(__file__).resolve().parent.parent
folder_entities = root / "entities"
folder = Path(__file__).resolve().parent
folder_input = folder / "input"
folder_output = folder / "output"
# create the output folder if it does not exist
os.makedirs(folder_output, exist_ok=True)

dlite.storage_path.append(f'{folder_entities/"performance"}/*.json')

print('dlite version =', dlite.__version__)

def test_create_input():
    """
    test the creation of an input file from a list of temperatures
    """

    # namespace
    ns = 'http://onto-ns.com/meta/0.1/SOFC_parameter_generation'

    paramgen = dlite.Instance.from_metaid(ns,dims={})

    default_values = {
            "nsnaps": 512,
            # geometrical parameters
            "L_channel": [10.0e-3,5.0e-3,15.0e-3],  #m
            "H_channel": [0.5e-3,0.25e-3,0.75e-3],  #m
            "W_channel": [0.5e-3,0.25e-3,0.75e-3],  #m
            "W_rib": [ 0.5e-3,0.25e-3,0.75e-3],  #m
            "H_Electrolyte": [1.0e-4,0.5e-4,1.5e-4],  #m
            "H_GDE": [1.0e-4,0.5e-4,1.5e-4],  #m
            # property parameters     
            "Por_cathode": [0.4,0.2,0.6],   #au
            "Tor_cathode": [4.5,1.5,7.5],   #au
            "Per_cathode": [100.0,10.0,300.0], #um^2
            "Spa_cathode": [1.0,0.5,1.5],   #1/nm
            "Por_anode": [0.4,0.2,0.6],   #au
            "Tor_anode": [4.5,1.5,7.5],   #au
            "Per_anode": [100.0,10.0,300.0], #um^2
            "Spa_anode": [1.0,0.5,1.5],   #1/nm
            "Sigma_cathode": [1.0e+3,1.0e+2,1.0e+4],    #S/m
            "Thc_cathode": [0.5,1.0,2.0], #J/smK
            "Sigma_anode": [1.0e+3,1.0e+2,1.0e+4],    #S/m
            "Thc_anode": [0.5,1.0,2.0], #J/smK
            # operation parameters
            "Prd_anode": [2.0,1.0,4.0], #Pa
            "Prd_cathode": [6.0,4.5,8.0], #Pa
            "Prs_GDE": [1.0,0.9,1.5],   #atm
            "Tmp_GDE": [1073.2,800.0,1200.0], #K
    }

    # populate the instance
    for key,value in default_values.items():
        if key != "nsnaps":
            paramgen[key+"_ref"] = value[0]
            paramgen[key+"_min"] = value[1]
            paramgen[key+"_max"] = value[2]            
        else:
            paramgen.nsnaps = value

    filepath = folder_output / "test_create_input.json"
    dict0 = paramgen.asdict()
    dict0["uri"] = dict0.pop("uuid")
    
    with open(file=filepath,mode="w") as f:
        json.dump(dict0,f,indent=4)


def default_get_design_parameters():
    """
    default design parameters
    """
    filepath = folder_input / "example_designparameters.json"

    #dlite.storage_path.append(f'{filepath}')
    inst_genparams = dlite.Instance.from_url(f'json://{filepath}')

    return inst_genparams

def test_get_design_parameters():
    """
    test the conversion function
    """
    inst_genparams = default_get_design_parameters()

    nsnaps, params = get_design_parameters(inst_genparams)

    print(nsnaps,params)


def default_get_study_parameters(inst_genparams):
    """
    default values for the study parameters
    """
    nsnaps, params = get_design_parameters(inst_genparams)

    # create the values
    array_params = create_snaps(NB_Snaps=nsnaps, params=params)
    return array_params

def test_get_generated_parameters():
    """
    test getting the output entity
    """
    inst_genparams = default_get_design_parameters()

    array_params = default_get_study_parameters(inst_genparams)

    generated_parameters = get_generated_parameters(inputParameters=inst_genparams,
                                                    array_params=array_params,
                                                    label="test_study_00")

    filepath = folder_output / "test_create_generatedparameters.json"
    dict0 = generated_parameters.asdict()
    dict0["uri"] = dict0.pop("uuid")
    
    with open(file=filepath,mode="w") as f:
        json.dump(dict0,f,indent=4)



if __name__ == "__main__":

    #test_create_input()

    #test_get_design_parameters()

    test_get_generated_parameters()