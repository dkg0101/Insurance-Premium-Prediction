
class InsuranceModel:
    def __init__(self,preprocessor,model) :
        try:
            self.preprocessor  = preprocessor
            self.regressor = model

        except Exception as e:
            raise e
        
        def predict(self,x):
            try:
                x_transformed = self.preprocessor.transform(x)
                y_hat = self.regressor.predict(x_transformed)

                return y_hat
            
            except Exception as e:
                raise e