from logging import debug
from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/car', methods=['GET'])
def car():
    return render_template('car.html')


@app.route('/car/pred', methods=['GET', 'POST'])
def car_pred():
    if request.method == "POST":
        try:
            owner = request.form.get('owner')
            km = request.form.get('km')
            price = float(request.form.get('price'))
            age = request.form.get('age')
            fuel = request.form.get('fuel')
            seller = request.form.get('seller')
            Transmission = request.form.get('Transmission')
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 0
            Seller_Type_Individual = 0
            if(fuel == 'Petrol'):
                Fuel_Type_Petrol = 1
                Fuel_Type_Diesel = 0
            else:
                Fuel_Type_Petrol = 0
                Fuel_Type_Diesel = 1
            if(seller == 'Individual'):
                Seller_Type_Individual = 1
            else:
                Seller_Type_Individual = 0
            Transmission_Mannual = 0
            if(Transmission == 'Mannual'):
                Transmission_Mannual = 1
            car_model = pickle.load(open('pkl/car.pkl', 'rb'))
            prediction = car_model.predict(
                [[price, km, owner, age, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
            answer = round(prediction[0] - 0.9, 2)
            return render_template('car_pred.html', answer=answer)
        except:
            return render_template('error.html')
    else:
        return render_template('error.html')

@app.route('/flight', methods=['POST', 'GET'])
def flight():
    return render_template('flight.html')

@app.route('/flight/pred', methods=['POST', 'GET'])
def flight_pred():
    if request.method == 'POST':
        try:
            Airline = request.form.get('Airline')
            Airline_Air_India = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_Jet_Airways = 0
            Airline_Jet_Airways_Business = 0
            Airline_Multiple_carriers = 0
            Airline_Multiple_carriers_Premium_economy = 0
            Airline_SpiceJet = 0
            Airline_Trujet = 0
            Airline_Vistara = 0
            Airline_Vistara_Premium_economy = 0
            if Airline == 'Jet Airways':
                Airline_Jet_Airways = 1
            elif Airline == 'IndiGo':
                Airline_IndiGo = 1
            elif Airline == 'Air India':
                Airline_Air_India = 1
            elif Airline == 'Multiple carriers':
                Airline_Multiple_carriers = 1
            elif Airline == 'SpiceJet':
                Airline_SpiceJet = 1
            elif Airline == 'Vistara':
                Airline_Vistara = 1
            elif Airline == 'Multiple carriers Premium economy':
                Airline_Multiple_carriers_Premium_economy = 1
            elif Airline == 'GoAir':
                Airline_GoAir = 1
            elif Airline == 'Jet Airways Business':
                Airline_Jet_Airways_Business = 1
            elif Airline == 'Vistara Premium economy':
                Airline_Vistara_Premium_economy = 1
            elif Airline == 'Trujet':
                Airline_Trujet = 1
            Date_of_Journey = request.form.get('Date_of_Journey')
            Journey_day = int(pd.to_datetime(
                Date_of_Journey, format="%Y-%m-%dT%H:%M").day)
            Journey_month = int(pd.to_datetime(
                Date_of_Journey, format="%Y-%m-%dT%H:%M").month)

            Source = request.form.get('Source')
            Source_Chennai = 0
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            if Source == 'Chennai':
                Source_Chennai = 1
            elif Source == 'Delhi':
                Source_Delhi = 1
            elif Source == 'Kolkata':
                Source_Kolkata = 1
            elif Source == 'Mumbai':
                Source_Mumbai = 1

            Destination = request.form.get('Destination')
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
            Destination_New_Delhi = 0
            if Destination == 'Cochin':
                Destination_Cochin = 1
            elif Destination == 'Delhi':
                Destination_Delhi = 1
            elif Destination == 'Hyderabad':
                Destination_Hyderabad = 1
            elif Destination == 'New_Delhi':
                Destination_New_Delhi = 1
            elif Destination == 'Kolkata':
                Destination_Kolkata = 1
            
            Dep_Time = request.form.get('Dep_Time')
            Dep_hour = int(pd.to_datetime(Dep_Time, format="%H:%M").hour)
            Dep_min = int(pd.to_datetime(Dep_Time, format="%H:%M").minute)
            Arrival_Time = request.form.get('Arrival_Time')
            Arrival_hour = int(pd.to_datetime(Arrival_Time, format="%H:%M").hour)
            Arrival_min = int(pd.to_datetime(Arrival_Time, format="%H:%M").minute)
            dur_hour = int(abs(Arrival_hour - Dep_hour))*60
            duration = int(abs(Arrival_min - Dep_min)) + dur_hour
            
            Total_Stops = request.form.get('Total_Stops')
            model = pickle.load(open('pkl/flight.pkl', 'rb'))
            prediction = model.predict([[
                duration, Total_Stops,Journey_day, Journey_month,
                Dep_hour, Dep_min, Arrival_hour, Arrival_min, Airline_Air_India,
                Airline_GoAir, Airline_IndiGo, Airline_Jet_Airways, Airline_Jet_Airways_Business, Airline_Multiple_carriers,
                Airline_Multiple_carriers_Premium_economy, Airline_SpiceJet, Airline_Trujet, Airline_Vistara,
                Airline_Vistara_Premium_economy,Source_Chennai,Source_Delhi,Source_Kolkata,
                Source_Mumbai,Destination_Cochin,Destination_Delhi,Destination_Hyderabad,
                Destination_Kolkata,Destination_New_Delhi
            ]])
            output = round(prediction[0], 2)
            print(output)
            return render_template('flight_pred.html', ans = output)
        except:
            return render_template('error.html')
    else:
        return render_template('error.html')

@app.route('/insurance', methods=['POST', 'GET'])
def insurance():
   return render_template('insurance.html')

@app.route('/insurance/pred', methods=['POST', 'GET'])
def insurance_pred():
    if request.method == 'POST':
        try:
            age = int(request.form.get('age'))
            gender = request.form.get('gender')
            if gender == 'Male':
                gender = 1
            else:
                gender = 0
            bmi = float(request.form.get('bmi'))
            children = int(request.form.get('children'))
            smoker = request.form.get('smoker')
            if smoker == 'Male':
                smoker = 1
            else:
                smoker = 0
            region = request.form.get('region')
            if region == 'India':
                region = 0
            elif region == "USA":
                region = 1
            elif region == "Canada":
                region = 1
            else:
                region = 3
            print('-'*50)
            model = pickle.load(open('pkl/insurance.pkl', 'rb'))
            pred = model.predict([[age, gender, bmi, children, smoker, region]])
            output = round(pred[0], 2)
            return render_template('insurance_pred.html', ans=output)
        except:
            return render_template('error.html')
    else:
        return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)
