from flask import Flask,render_template,request,jsonify
from src.insurance.utils.main_utlls import load_object
from src.insurance.ml.model import InsuranceData,InsuranceModel,ModelResolver
from src.insurance.logger import logging
from src.insurance.exception import CustomException
from src.insurance.constant import SAVED_MODEL_DIR
import pandas as pd 
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

        print('received data is,', age,sex,bmi,children,smoker,region)

        insurance_data = InsuranceData(age=age,
                                       sex=sex,
                                       bmi=bmi,
                                    children=children,
                                    smoker=smoker,
                                    region=region)
        print(insurance_data.__dict__)
        

        input_df = insurance_data.get__input_data_frame()
        model_resolver = ModelResolver()
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)

        # Make prediction using the model and input data
        predicted_premium = model.predict(input_df)
        print(f"Predicted premium is: {predicted_premium} and type ooutput is {type(predicted_premium)}")

        # Prepare response with predicted premium
        response = {
            'premium': f"{round(predicted_premium[0],3)} Rs",
            'input_data': insurance_data.__dict__
            }

        return render_template('result.html', response=response)
    except Exception as e:
        raise CustomException(e,sys)

if __name__ == "__main__":
    app.run(debug=True)



