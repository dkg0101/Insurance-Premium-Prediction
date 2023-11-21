from src.insurance.configuration.mongo_db_connection import MongoDBClient
from src.insurance.constant.database import DATABASE_NAME
from src.insurance.exception import CustomException
from src.insurance.logger import logging
from typing import Optional

import sys
import pandas as pd
import numpy as np

class Insurance_Data:
    def __init__(self) :
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise CustomException(e,sys)
        
   
        
    def export_collection_as_dataframe(
            self,collection_name:str,database_name:Optional[str]=None) -> pd.DataFrame:
        """
            This function export entire collection as dataframe:
            return pd.DataFrame of collection
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]
            
            logging.info('Creating pandas dataframe')
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                logging.info('Dropping unnecessary columns')
                
                df = df.drop(columns=["_id"], axis=1) 
            
            logging.info("Replacing null values with np.nan")
            df.replace({"na": np.nan}, inplace=True)
            logging.info(f"Successfully exported dataframe with shape:{df.shape}")

            return df       

        except Exception as e:
            raise CustomException(e,sys)
          
