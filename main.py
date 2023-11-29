from src.insurance.logger import logging
from src.insurance.exception import CustomException
from src.insurance.constant import DATABASE_NAME,COLLECTION_NAME

from src.insurance.configuration.mongo_db_connection import MongoDBClient
from src.insurance.pipeline.training_pipeline import TrainingPipeline



if __name__=='__main__':
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)
    