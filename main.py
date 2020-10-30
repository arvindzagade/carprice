from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('carpricemodel.pkl', 'rb'))
standard_to = StandardScaler()

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/predict", methods= ["POST"])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Age = 2020 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        ## TODO : Train model with log of KmsDriven
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol= request.form['Fuel_Type']
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else: # Fuel Type is CNG
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Seller_Type_Individual = request.form['Seller_Type']
        if( Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else: #Seller Type is Dealer
            Seller_Type_Individual = 0
        Transmission_Manual= request.form['Transmission_Type']
        if(Transmission_Manual == "Manual"):
            Transmission_Manual = 1
        else: # Transmission is Automatic
            Transmission_Manual =0
        # TODO : We never trained model on log of KmsDriven , so TRY that
        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Age, Fuel_Type_Diesel,
       Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round(prediction[0],2)
        if output<0:
            return render_template('index.html', prediction_text="Sorry you cannot sell this car !")
        else:
            return render_template('index.html', prediction_text="You can sell this car at {} lakhs !!".format(output))
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
