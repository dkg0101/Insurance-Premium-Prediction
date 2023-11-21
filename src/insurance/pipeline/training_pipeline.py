from src.insurance.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig
from src.insurance.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.insurance.exception import CustomException
from src.insurance.logger import logging
from src.insurance.components.data_ingestion import DataIngestion
from src.insurance.components.data_validation import DataValidation
import sys,os

class TrainingPipeline:
    def __init__(self) :
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data ingestion started...")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"""Data Ingestion Completed and data ingestion artifact is:
            [{data_ingestion_artifact}]""")
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e,sys)

    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Validation started...")
            data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"""Data Validation Completed and data validation artifact is:
            [{data_validation_artifact}]""")
            
            return data_validation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)

    def start_data_transformation(self):
        try:
            pass
        except  Exception as e:
            raise  CustomException(e,sys)

    def start_model_trainer(self):
        try:
            pass
        except  Exception as e:
            raise  CustomException(e,sys)

    def start_model_evaluation(self):
        try:
            pass
        except  Exception as e:
            raise  CustomException(e,sys)

    def start_model_pusher(self):
        try:
            pass
        except  Exception as e:
            raise  CustomException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact = self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
        except  Exception as e:
            raise  CustomException(e,sys)