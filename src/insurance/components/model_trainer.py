from src.insurance.exception import CustomException
from src.insurance.logger import logging
from src.insurance.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from src.insurance.entity.config_entity import ModelTrainerConfig
from src.insurance.utils.main_utlls import save__object,load_object,load_numpy_array_data
from src.insurance.ml.metric import get_performance_metric
from src.insurance.ml.model  import InsuranceModel
from xgboost import XGBRegressor
import os,sys

class ModelTrainer:
    def __init__(self,data_tarnsformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig) :
        try:
            self.model_trainer_config =  model_trainer_config
            self.data_transformation_artifact = data_tarnsformation_artifact
            
        except Exception as e:
            raise CustomException(e,sys)
        
    
    
        
    def train_model(self,X_train,y_train):
        try:
            xgb_regressor = XGBRegressor(learning_rate=0.05, n_estimators = 64)
            xgb_regressor.fit(X_train,y_train)

            return xgb_regressor

        except Exception as e:
            raise CustomException(e,sys)
        


        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("!! Model Training Initiated....")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info("Loading train,test numpy array")
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train,y_train,X_test,y_test = (train_arr[:,:-1],
                                             train_arr[:,-1],
                                             test_arr[:,:-1],
                                             test_arr[:,-1]
                                             )
            
            logging.info("Training ML model on data")
            model = self.train_model(X_train=X_train,y_train=y_train)
            y_train_pred = model.predict(X_train)

            performance_train_metric = get_performance_metric(y_true=y_train,y_pred= y_train_pred)

            if performance_train_metric.R2_socre < self.model_trainer_config.expected_r2_score:
                raise Exception("Trained model is not good to provide expected accuracy")
            

            y_test_pred = model.predict(X_test)
            performance_test_metric = get_performance_metric(y_true=y_test,y_pred=y_test_pred)

            logging.info("Checking Underfitting,Overfitting")
            diff = abs(performance_train_metric.R2_socre - performance_test_metric.R2_socre)

            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good! try to do more experimentation")
            
            logging.info(f'Saving Model object at: {self.model_trainer_config.trained_model_file_path} ')

            preprocessor = load_object(self.data_transformation_artifact.preprocessor_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            insurance_model = InsuranceModel(preprocessor=preprocessor,model=model)
            save__object(file_path=self.model_trainer_config.trained_model_file_path,obj=insurance_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact= performance_train_metric,
                test_metric_artifact= performance_test_metric
            )

            logging.info(f"Model trainer Artifact: {model_trainer_artifact}")

            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
    