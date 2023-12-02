from src.insurance.exception import CustomException
from src.insurance.logger import logging
from src.insurance.entity.config_entity import ModelEvaluationConfig
from src.insurance.entity.artifact_entity import ModelTrainerArtifact,ModelEvaluationArtifact,DataValidationArtifact
from src.insurance.ml.metric.regression_metric import get_performance_metric
from src.insurance.ml.model.estimator import InsuranceModel,ModelResolver
from src.insurance.constant.training_pipeline import TARGET_COLUMN
from src.insurance.utils.main_utlls import load_object,write_yaml_file

import pandas as pd
import os,sys


class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                 data_validation_artifact:DataValidationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact
                ):
        try:
            self.model_trainer_artifact = model_trainer_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_evaluation_config  = model_evaluation_config

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_evaluation(self):
        try:
            valid_train_file_path = self.data_validation_artifact.valid_data_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_data_test_file_path

            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df,test_df])
            y_true = df[TARGET_COLUMN]
            
            df.drop(columns=[TARGET_COLUMN],axis=1,inplace=True)

            trained_model_file_path = self.model_trainer_artifact.trained_model_path
            model_resolver = ModelResolver()
            is_model_accepted = True

            if not  model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuaracy= None,
                    best_model_path = None,
                    trained_model_path= trained_model_file_path,
                    best_model_metric_artifact=None,
                    trained_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact                
                )
                logging.info(f"model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            
            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(latest_model_path)
            latest_model_y_pred = latest_model.predict(df)
            latest_model_performance_metric = get_performance_metric(y_true,latest_model_y_pred)


            trained_model = load_object(trained_model_file_path)
            trained_model_y_pred = trained_model.predict(df)
            trained_model_performance_metric = get_performance_metric(y_true,trained_model_y_pred)

            

            improved_accuracy = trained_model_performance_metric.R2_socre - latest_model_performance_metric.R2_socre 

            if improved_accuracy < self.model_evaluation_config.change_threshold:
                is_model_accepted = False
            else:
                is_model_accepted = True
            
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuaracy=improved_accuracy,
                best_model_path = latest_model_path,
                trained_model_path= trained_model_file_path,
                trained_model_metric_artifact=trained_model_performance_metric,
                best_model_metric_artifact= latest_model_performance_metric
            )
            logging.info(f"model evaluation artifact: {ModelEvaluationArtifact}")

            logging.info("Saving model evaluation report")
            model_evaluation_report = model_evaluation_artifact.__dict__
            os.makedirs(self.model_evaluation_config.model_evaluation_dir,exist_ok=True)
            

            # logging.info(f"Saving model evaluation report at: {self.model_evaluation_config.model_evaluation_report_file_path}")
            # write_yaml_file(file_path=self.model_evaluation_config.model_evaluation_report_file_path,content=model_evaluation_report)

            return model_evaluation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)

        