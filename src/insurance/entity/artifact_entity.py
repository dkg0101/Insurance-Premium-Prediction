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

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path:str
    transformed_test_file_path:str
    preprocessor_object_file_path:str

@dataclass
class RegressionMetricArtifact:
    R2_socre:float
    RMSE:float

@dataclass
class ModelTrainerArtifact:
    trained_model_path:str
    train_metric_artifact: RegressionMetricArtifact
    test_metric_artifact: RegressionMetricArtifact


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuaracy:float
    best_model_path:str
    trained_model_path:str
    best_model_metric_artifact:RegressionMetricArtifact
    trained_model_metric_artifact:RegressionMetricArtifact

@dataclass
class ModelPusherArtifact:
    saved_model_path:str
    model_file_path:str