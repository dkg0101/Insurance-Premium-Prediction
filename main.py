from insurance.logger import logging
from insurance.exception import CustomException
from insurance.constant import DATABASE_NAME,COLLECTION_NAME
from data_dump import dump_data_to_mongodb

file_path= "insurance.csv"
if __name__=="__main__":
    dump_data_to_mongodb(file_path=file_path,database_name=DATABASE_NAME,collection_name=COLLECTION_NAME)


