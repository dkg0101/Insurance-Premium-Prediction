import os

#defining common constant variable for training pipeline
TARGET_COLUMN = 'expenses'
PIPELINE_NAME = 'insurance'
ARTIFACT_DIR = 'artifacts'
DATA_FILE_NAME = 'data.csv'

TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'

PREPROCESSING_OBJECT_FILE_NAME = 'preprocessor.pkl'
MODEL_FILE_NAME = 'model.pkl'
SCHEMA_FILE_PATH =os.path.join('config','schema.yaml')
SAVED_MODEL_DIR = 'saved_models'

# "Data Ingestion related constants"

DATA_INGESTION_COLLECTION_NAME:str = 'insurance'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str = 'feature_store'
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


# "Data Validation related constants"

DATA_VALIDATION_DIR_NAME:str = 'data_validation'
DATA_VALIDATION_VALID_DIR:str = 'validated'
DATA_VALIDATION_INVALID_DIR:str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR:str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = 'report.yaml'

# Data transformation related constants 
DATA_TRANSFORMATION_DIR_NAME = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = 'transformed'
DATA_TRANSFORMATION_PREPROCESSOR_OBJECT_DIR:str = 'preprocessor_object'

# Model Trainer related constants
MODEL_TRAINER_DIR_NAME: str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'
MODEL_TRAINER__EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDER_FITTING_THRESHOLD:float = 0.05

# Model Evaluation related constants
MODEL_EVALUATION_DIR_NAME:str = 'model_evaluation'
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float = 0.02
MODEL_EVALUATION_REPORT_NAME:str = 'report.yaml'


# Model Pusher related constants
MODEL_PUSHER_DIR_NAME = 'model_pusher'
MODEL_PUSHER_SAVED_MODEL = SAVED_MODEL_DIR
