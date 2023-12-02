import yaml
from src.insurance.exception import CustomException
from src.insurance.logger import logging
import os,sys
import numpy as np
import dill

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)
    

def write_yaml_file(file_path:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
            
    except Exception as e:
        CustomException(e,sys)

def save_numpy_array_data(file_path:str,array:np.array):
    """
    This function helps to save  data in numpy array form
    to the given location
    params: 
    file_path:str:location to save file
    array:np.array: data to save as file
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as np_file:
            np.save(np_file,array)
            
    except Exception as e:
        CustomException(e,sys)

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e

def save__object(file_path:str,obj:object) :
    try:
        logging.info("Saving object using save_object method of main utils")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info(f"Object saved at: {file_path} ")
    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"Object not found!, {file_path} does not exists")
        
        with open(file_path, "rb") as file_obj:
            
            return dill.load(file_obj)
            
    except Exception as e:
        raise CustomException(e, sys) from e