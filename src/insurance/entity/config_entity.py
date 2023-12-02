import os,sys
from datetime import datetime
from src.insurance.constant import training_pipeline
from src.insurance.exception import CustomException


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()) :
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

        self.pipeline_name:str = training_pipeline.PIPELINE_NAME
        self.artifact_dir:str = os.path.join(training_pipeline.ARTIFACT_DIR,timestamp)
        self.timestamp:str = timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig) :
        try:
            self.data_ingestion_dir:str = os.path.join(
                training_pipeline_config.artifact_dir,
                training_pipeline.DATA_INGESTION_DIR_NAME,
            )

            self.feature_store_file_path:str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                training_pipeline.DATA_FILE_NAME
            )

            self.train_file_path:str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.TRAIN_FILE_NAME
            )
            self.test_file_path:str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.TEST_FILE_NAME
            )

            self.data_ingestion_collection_name:str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
            
            self.train_test_split_ratio:float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        
        except Exception as e:
            raise CustomException(e,sys)

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
            self.transformed_train_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    training_pipeline.TRAIN_FILE_NAME.replace('csv','npy') )
            self.transformed_test_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    training_pipeline.TEST_FILE_NAME.replace('csv','npy') )
            
            self.preprocessor_object_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_PREPROCESSOR_OBJECT_DIR,
                                                                  training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)


class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            try:
                self.model_trainer_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
                self.trained_model_file_path:str = os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                                training_pipeline.MODEL_FILE_NAME)
                self.expected_r2_score:float = training_pipeline.MODEL_TRAINER__EXPECTED_SCORE
                self.overfitting_underfitting_threshold:float = training_pipeline.MODEL_TRAINER_OVERFITTING_UNDER_FITTING_THRESHOLD
            
            except Exception as e:
                raise CustomException(e,sys)
            
class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_evaluation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_EVALUATION_DIR_NAME)
            self.model_evaluation_report_file_path:str = os.path.join(self.model_evaluation_dir,training_pipeline.MODEL_EVALUATION_REPORT_NAME)
            self.change_threshold: float = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

        except Exception as e:
            raise CustomException(e,sys)
        
class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig) :
        try:
            self.model_pusher_dir:str = os.path.join(
                training_pipeline_config.artifact_dir,training_pipeline.MODEL_PUSHER_DIR_NAME
            )
            
            self.model_file_path:str = os.path.join(self.model_pusher_dir,
                training_pipeline.MODEL_FILE_NAME
            )

            timestamp = round(datetime.now().timestamp())
            
            self.saved_model_path = os.path.join(
                training_pipeline.SAVED_MODEL_DIR,
                f"{timestamp}",
                training_pipeline.MODEL_FILE_NAME
            )

        except Exception as e:
            raise CustomException(e,sys)
    
