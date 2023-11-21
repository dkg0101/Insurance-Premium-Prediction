from src.insurance.logger import logging
from src.insurance.exception import CustomException
from src.insurance.constant.training_pipeline import SCHEMA_FILE_PATH
from src.insurance.entity import DataValidationConfig
from src.insurance.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.insurance.utils.main_utlls import read_yaml_file,write_yaml_file
from distutils import dir_util
from scipy.stats import ks_2samp
import pandas as pd
import sys,os

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig) :
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame) -> bool:
        try :
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Number of columns required:[{number_of_columns}]")
            logging.info(f"Number of columns present: [{len(dataframe.columns)}]")

            if number_of_columns==len(dataframe.columns):
                return True
            return False
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def is_numerical_columns_present(self,dataframe:pd.DataFrame) -> bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns

            all_numerical_columns_present = True
            missing_numerical_columns = []

            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    all_numerical_columns_present = False
                    missing_numerical_columns.append(num_column)

            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")

            return all_numerical_columns_present
        
        except Exception as e:
            raise CustomException(e,sys)

    def is_categorical_columns_present(self,dataframe:pd.DataFrame) -> bool:

        try:
            categorical_columns = self._schema_config['categorical_columns']
            dataframe_columns = dataframe.columns

            all_categorical_columns_present = True
            missing_categorical_columns = []

            for cat_column in categorical_columns:
                if cat_column not in dataframe_columns:
                    all_categorical_columns_present = False
                    missing_categorical_columns.append(cat_column)

            logging.info(f"Missing Categorical columns: [{missing_categorical_columns}]")

            return all_categorical_columns_present
        
        except Exception as e:
            raise CustomException(e,sys)

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            logging.info("Creating directory for drift report..")
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            logging.info(f"Drift report is saved and status is {status}")
            return status

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
            try:
                error_message = ""
                train_file_path = self.data_ingestion_artifact.trained_file_path
                test_file_path = self.data_ingestion_artifact.test_file_path

                logging.info("Reading data from train and test file location")
                train_dataframe = DataValidation.read_data(train_file_path)
                test_dataframe = DataValidation.read_data(test_file_path)

                logging.info("Validating number of columns for train dataframe")
                status = self.validate_number_of_columns(train_dataframe)
                if not status:
                    error_message = f"{error_message}Train dataframe does not contain all columns"

                logging.info("Validating number of columns for test dataframe")
                status = self.validate_number_of_columns(test_dataframe)
                if not status:
                    error_message = f"{error_message}Test Dataframe does not contain all columns"

                logging.info("Validating all numerical columns exists or not")
                status = self.is_numerical_columns_present(dataframe=train_dataframe)
                if not status:
                    error_message = f"{error_message}Train dataframe does not contain all numerical columns"
                
                status = self.is_numerical_columns_present(dataframe=test_dataframe)
                if not status:
                    error_message = f"{error_message}Test dataframe does not contain all numerical columns"
                
                
                logging.info("Validating all categorical columns exists or not")
                status = self.is_categorical_columns_present(dataframe=train_dataframe)
                if not status:
                    error_message = f"{error_message}Train dataframe does not contain all categorical columns"
                
                status = self.is_categorical_columns_present(dataframe=test_dataframe)
                if not status:
                    error_message = f"{error_message}Test dataframe does not contain all categorical columns"
                
                if len(error_message)>0:
                    raise Exception(error_message)
                
                detect_dataset_drift_status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

                data_validation_artifact = DataValidationArtifact(
                    validation_status = detect_dataset_drift_status,
                    valid_data_train_file_path=self.data_ingestion_artifact.trained_file_path,
                    valid_data_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_data_train_file_path=None,
                    invalid_data_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )

                logging.info(f"Data validation artifact: {data_validation_artifact}")

                return data_validation_artifact

            except Exception as e:
                raise CustomException(e,sys)
        
