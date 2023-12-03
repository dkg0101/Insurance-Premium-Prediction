from src.insurance.constant.training_pipeline import  SAVED_MODEL_DIR,MODEL_FILE_NAME
from src.insurance.exception import CustomException
import pandas as pd
import os,sys

class InsuranceData:
    def __init__(self,age:int,sex:str,bmi:float,
                children:int,smoker:str,region:str):
        try:
            self.age = age
            self.sex = sex
            self.bmi = bmi
            self.children = children
            self.smoker = smoker
            self.region = region
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_input_data_dict(self):
        try:
            input_data = {
                'age': self.age,
                'sex': self.sex,
                'bmi': self.bmi,
                'children':self. children,
                'smoker':  self.smoker,
                'region':  self.region }
            
            return input_data
        
        except Exception as e:
            CustomException(e,sys)

    def get__input_data_frame(self):

        try:
            input_dict = self.get_input_data_dict()
            print(input_dict)
            return pd.DataFrame(input_dict,index=[1])
        
        except Exception as e:
            raise CustomException(e, sys) from e


class ModelResolver:

    def __init__(self,model_dir = SAVED_MODEL_DIR) :
        try:
           self.model_dir = model_dir
        
        except Exception as e:
            raise e
            
    def get_best_model_path(self):
        """
        This function will listdown all saved models ascendingly
        and return latest model path
        """
        try:
            timestamps = list(map(int,os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME)
            return latest_model_path
        except Exception as e:
            raise e
    
    def is_model_exists(self) -> bool:
        try:
            if not os.path.exists(self.model_dir):
                return False
            
            timestamps = os.listdir(self.model_dir)

            if len(timestamps) ==0:
                return False
            
            latest_model_path = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False
            
            return True
        
        except Exception as e:
            raise e



class InsuranceModel:
    def __init__(self,preprocessor,model) :
        try:
            self.preprocessor  = preprocessor
            self.regressor = model

        except Exception as e:
            raise e
        
    def predict(self,x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_hat = self.regressor.predict(x_transformed)

            return y_hat
        
        except Exception as e:
            raise e
        

    
