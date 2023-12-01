from src.insurance.exception import CustomException
from src.insurance.logger import logging
from src.insurance.entity.artifact_entity import RegressionMetricArtifact
from sklearn.metrics import mean_squared_error,r2_score
import sys

def get_performance_metric(y_true,y_pred) -> RegressionMetricArtifact:
    try:
        model_R2_score = r2_score(y_true=y_true,y_pred=y_pred)
        model_root_mean_squared_error = mean_squared_error(y_true=y_true,y_pred=y_pred)

        logging.info(f"R2 score is: {model_R2_score} and RMSE: {model_root_mean_squared_error}")
        performance_metric = RegressionMetricArtifact(
            R2_socre= model_R2_score,
            RMSE= model_root_mean_squared_error)
        
        return performance_metric
    
    except Exception as e:
        raise CustomException(e,sys)