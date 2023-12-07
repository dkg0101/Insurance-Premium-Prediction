from flask import Flask,render_template,request,jsonify
from src.insurance.utils.main_utlls import load_object
from src.insurance.pipeline.training_pipeline import TrainingPipeline
from src.insurance.ml.model import InsuranceData,InsuranceModel,ModelResolver
from src.insurance.logger import logging
from src.insurance.exception import CustomException
from src.insurance.constant import SAVED_MODEL_DIR
from src.insurance.constant.application import APP_HOST,APP_PORT
import pandas as pd 
import numpy as np
import os,sys
app = Flask(__name__)




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-prediction",methods=["POST"])
def get_prediction():
  return render_template("predict.html")



@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Access form data using request.form
        age = int(request.form["age"])
        sex = request.form["sex"]
        bmi = float(request.form["bmi"])
        children = int(request.form["children"])
        smoker = request.form["smoker"]
        region = request.form["region"]


        insurance_data = InsuranceData(age=age,
                                       sex=sex,
                                       bmi=bmi,
                                    children=children,
                                    smoker=smoker,
                                    region=region)
        logging.info(f"Input data is {insurance_data.__dict__}")
        

        input_df = insurance_data.get__input_data_frame()
        model_resolver = ModelResolver()
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)

        # Make prediction using the model and input data
        predicted_premium = model.predict(input_df)

        logging.info(f"Predicted premium is: {int(predicted_premium)} and type ootput is {type(predicted_premium)}")

        # Prepare response with predicted premium
        response = {
            'premium': f"{int(predicted_premium)}",
            'input_data': insurance_data.__dict__
            }

        return render_template('result.html', response=response)
    except Exception as e:
        raise CustomException(e,sys)
    


if __name__ == "__main__":
    app.run(host=APP_HOST,port=APP_PORT)



