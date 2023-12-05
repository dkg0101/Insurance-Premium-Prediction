from src.insurance.logger import logging
from src.insurance.exception import CustomException
from src.insurance.entity.config_entity import DataTransformationConfig
from src.insurance.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from src.insurance.constant.training_pipeline import TARGET_COLUMN
from src.insurance.utils.main_utlls import save__object,save_numpy_array_data
from sklearn.preprocessing import RobustScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
import os,sys


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact) -> None:
        """
        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        

        except Exception as e:
            raise CustomException(e,sys)
 
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise CustomException(e, sys) 

    @classmethod
    def get_data_transformer_object(cls):
        try: 
            numerical_columns =  ['age', 'bmi']
            categorical_columns = ['sex', 'smoker', 'region']
 
            num_pipeline = Pipeline(
                steps=[
                ('simple_imputer',SimpleImputer(strategy="constant", fill_value=0)),
                ('scaler',RobustScaler())
                ]
                )
            
            cat_pipeline = Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('oneHotEncoder',OneHotEncoder())
                ]
                )

            logging.info(f"Numerical Columns are : {numerical_columns}")
            logging.info(f"Categorical Columns are : {categorical_columns}")

            preprocessor = ColumnTransformer(
                transformers=
                [('num_trf',num_pipeline,numerical_columns),
                ('cat_trf',cat_pipeline,categorical_columns)],
                remainder='passthrough')

            return preprocessor 

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_tranformation(self) -> DataTransformationArtifact:
        try:
            logging.info('Initiating data transformation..')
            logging.info('Loading valid data')
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_data_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_data_train_file_path)


            #training data
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            #testing data
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info('Applying preprocessing steps..')
            preprocessor = self.get_data_transformer_object()
            
            proprocessor_object = preprocessor.fit(input_feature_train_df)

            transformed_train = proprocessor_object.transform(input_feature_train_df)
            transformed_test = proprocessor_object.transform(input_feature_test_df)

            
            #save numpy array data
            train_arr = np.c_[transformed_train,target_feature_train_df]
            test_arr = np.c_[transformed_test,target_feature_test_df]


            logging.info(f'Saving numpy array trainig data at: {self.data_transformation_config.transformed_train_file_path} ')
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)

            logging.info(f"Saving numpy array test data at: {self.data_transformation_config.transformed_test_file_path}")
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)

            logging.info(f"Saving preprocessor object at: {self.data_transformation_config.preprocessor_object_file_path}")
            save__object( self.data_transformation_config.preprocessor_object_file_path,obj=proprocessor_object)


            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessor_object_file_path=self.data_transformation_config.preprocessor_object_file_path)
            
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")

            return data_transformation_artifact



        except Exception as e:
            raise CustomException(e,sys)
    
    



    