from src.insurance.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,\
DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from src.insurance.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,\
DataTransformationArtifact, ModelTrainerArtifact,ModelPusherArtifact, ModelEvaluationArtifact 
from src.insurance.exception import CustomException
from src.insurance.logger import logging
from src.insurance.components.data_ingestion import DataIngestion
from src.insurance.components.data_validation import DataValidation
from src.insurance.components.data_transformation import DataTransformation
from src.insurance.components.model_trainer import ModelTrainer
from src.insurance.components.model_evaluation import ModelEvaluation
from src.insurance.components.model_pusher import ModelPusher
from src.insurance.cloud_storage.s3_syncer import S3Sync
from src.insurance.constant.s3_bucket import TRAINING_BUCKET_NAME
from src.insurance.constant.training_pipeline import SAVED_MODEL_DIR
import sys,os


class TrainingPipeline:
    is_pipeline_running=False

    def __init__(self) :
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

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

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("Data transformation started")
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_tranformation()

            logging.info("Data transformation Completed")
            return data_transformation_artifact
        
        except  Exception as e:
            raise  CustomException(e,sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try: 
            logging.info("Model training process started...")
            model_training_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(data_tarnsformation_artifact=data_transformation_artifact,
                                         model_trainer_config=model_training_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model training Completed.")
            return model_trainer_artifact
        
        except  Exception as e:
            raise  CustomException(e,sys)

    def start_model_evaluation(self,model_trainer_artifact:ModelTrainerArtifact,
                               data_validation_artifact:DataValidationArtifact)-> ModelEvaluationArtifact:
        try:
            logging.info("Model Evaluation Process started..")
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                               data_validation_artifact=data_validation_artifact,model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info("Model Evaluation completed.")
            return model_evaluation_artifact
        
        except  Exception as e:
            raise  CustomException(e,sys)

    def start_model_pusher(self,model_evluation_artifact:ModelEvaluationArtifact)-> ModelPusherArtifact:
        try:
            logging.info("Model Puhser Started..")
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                       model_evaluation_artifact=model_evluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()

        except  Exception as e:
            raise  CustomException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            logging.info("Storing artifact dir at S3 bucket")
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
    
    def sync_saved_model_dir_to_s3(self):
        try:
            logging.info("Storing saved model at s3 bucket")
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            logging.info("Training Pipeline Initiated..")
            TrainingPipeline.is_pipeline_running=True
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact = self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact:ModelEvaluationArtifact = self.start_model_evaluation(model_trainer_artifact=model_trainer_artifact,data_validation_artifact=data_validation_artifact)

            if not model_evaluation_artifact.is_model_accepted :
                raise Exception("Existing model is better than newly trained Model ")
            model_pusher_artifact:ModelPusherArtifact = self.start_model_pusher(model_evluation_artifact=model_evaluation_artifact)
            TrainingPipeline.is_pipeline_running=False
            
            logging.info("Training pipeline Completed.")
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()

        except  Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainingPipeline.is_pipeline_running=False
            raise  CustomException(e,sys)