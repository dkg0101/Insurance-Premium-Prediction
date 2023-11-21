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


"Data Ingestion related constants"
DATA_INGESTION_COLLECTION_NAME:str = 'insurance'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str = 'feature_store'
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


"Data Validation related constants"

DATA_VALIDATION_DIR_NAME:str = 'data_validation'
DATA_VALIDATION_VALID_DIR:str = 'validated'
DATA_VALIDATION_INVALID_DIR:str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR:str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = 'report.yaml'
