from insurance.logger import logging
from insurance.exception import CustomException
from insurance.configuration.mongo_db_connection import MongoDBClient
from insurance.constant.database import DATABASE_NAME
from pathlib import Path
import pymongo 
import pandas as pd
import os,sys

def dump_data_to_mongodb(file_path:str,database_name:str,collection_name:str):
        """"
        This function takes path of csv data file and stores
        records into MongoDB database as a documents
        """
        try:
            logging.info('Data insertion process starts...')
            logging.info('Reading csv file as pandas DataFrame')
            df = pd.read_csv(Path(file_path))

            logging.info("Converting df to list of dictionaries")
            data = df.to_dict(orient='records')

            
            mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            mongo_client = MongoDBClient(database_name=DATABASE_NAME)

            if database_name is None:
                collection = mongo_client.client[collection_name]
            else:
                collection = mongo_client.client[database_name][collection_name]
           
            logging.info("Inserting data into database..")
            collection.insert_many(data)
            mongo_client.client.close()
            logging.info(f"Data inserted into collection:'{collection_name}' successfully.")

        except Exception as e:
            raise CustomException(e,sys)
        