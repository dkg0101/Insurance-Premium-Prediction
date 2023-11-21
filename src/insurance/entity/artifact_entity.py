from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_data_train_file_path:str
    valid_data_test_file_path:str
    invalid_data_train_file_path:str
    invalid_data_test_file_path:str
    drift_report_file_path:str