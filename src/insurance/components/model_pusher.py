from src.insurance.exception import CustomException 
from src.insurance.logger import logging
from src.insurance.entity.config_entity import ModelPusherConfig
from src.insurance.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
import shutil,os,sys

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_evaluation_artifact:ModelEvaluationArtifact
                 ) :
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
            

        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_model_pusher(self):
        """
        This function  will save accepted model from Evaluation stage
        to the saved_models directory 
        """
        try:
            logging.info("Model Pusher stage Activated..")
            trained_model_path = self.model_evaluation_artifact.trained_model_path

            logging.info("Saving trained model to model pusher directory")
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=model_file_path)

            logging.info("Saving model into 'saved_models' directory")
            saved_model_file_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=saved_model_file_path)

            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_file_path,
                                                        model_file_path=model_file_path)
            logging.info(f"Model Pusher Artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        
        except Exception as e:
            raise CustomException(e,sys)