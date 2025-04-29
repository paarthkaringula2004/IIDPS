import sys
import pandas as pd
import numpy as np
import pickle

class Detection:

    def main(calls, modelfile="rf_model.sav"):
        
        filename=modelfile
        train = pickle.load(open(filename, 'rb'))
        predicted_class = train.predict([calls])
        print(predicted_class[0])
        print("Successfully Predicted")
        return predicted_class[0]
        
if __name__ == "__main__":
    Detection.main('ldrloaddll ldrgetprocedureaddress ldrloaddll ldrgetprocedureaddress ldrgetprocedureaddress ldrgetprocedureaddress ldrgetprocedureaddress ldrgetprocedureaddress ')
    
    

