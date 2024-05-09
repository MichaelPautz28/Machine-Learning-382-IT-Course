#!/usr/bin/env python
# coding: utf-8

# 
# 

# In[5]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pickle
 
# Load the model
with open('artifacts/model_2.pkl', 'rb') as f:
    model = pickle.load(f)
 
#Initialise the Dash App
app = dash.Dash(__name__)
 
#Define App Layout
app.layout = html.Div([
    html.H1("Loan Eligibility Predictor"),
    html.Label("Gender:"),
    dcc.Dropdown(
        id='gender',
        options=[
            {'label': 'Male', 'value': 1},
            {'label': 'Female', 'value': 0}
        ],
        value=1
    ),
    html.Label("Married:"),
    dcc.Dropdown(
        id='married',
        options=[
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0}
        ],
        value=1
    ),
    html.Label("Dependents:"),
    dcc.Dropdown(
        id='dependents',
        options=[
            {'label': '0', 'value': 0},
            {'label': '1', 'value': 1},
            {'label': '2', 'value': 2},
            {'label': '3+', 'value': 3}
        ],
        value=0
    ),
    html.Label("Education:"),
    dcc.Dropdown(
        id='education',
        options=[
            {'label': 'Graduate', 'value': 'Graduate'},
            {'label': 'Non Graduate', 'value': 'Non Graduate'}
        ],
        value='Graduate'
    ),
    html.Label("Self Employed:"),
    dcc.Dropdown(
        id='self_employed',
        options=[
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0}
        ],
        value=0
    ),
    html.Label("Applicant Income:"),
    dcc.Input(id='applicant_income', type='number', value=0),
    html.Label("Coapplicant Income:"),
    dcc.Input(id='coapplicant_income', type='number', value=0),
    html.Label("Loan Amount:"),
    dcc.Input(id='loan_amount', type='number', value=0),
    html.Label("Loan Amount Term:"),
    dcc.Dropdown(
        id='loan_amount_term',
        options=[
            {'label': '12 months', 'value': 12},
            {'label': '36 months', 'value': 36},
            {'label': '60 months', 'value': 60},
            {'label': '84 months', 'value': 84},
            {'label': '120 months', 'value': 120},
            {'label': '180 months', 'value': 180},
            {'label': '240 months', 'value': 240},
            {'label': '300 months', 'value': 300},
            {'label': '360 months', 'value': 360},
            {'label': '480 months', 'value': 480}
        ],
        value=360
    ),
    html.Label("Credit History:"),
    dcc.Dropdown(
        id='credit_history',
        options=[
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0}
        ],
        value=1
    ),
    html.Label("Property Area:"),
    dcc.Dropdown(
        id='property_area',
        options=[
            {'label': 'Rural', 'value': 'Rural'},
            {'label': 'Semiurban', 'value': 'Semiurban'},
            {'label': 'Urban', 'value': 'Urban'}
        ],
        value='Rural'
    ),
    html.Button('Check Eligibility', id='submit-val', n_clicks=0),
    html.Div(id='output')
])
 
 
# Define Callback Function for Predictions
@app.callback(
    Output('output', 'children'),
    Input('submit-val', 'n_clicks'),
    [Input('gender', 'value'),
        Input('married', 'value'),
        Input('dependents', 'value'),
        Input('education', 'value'),
        Input('self_employed', 'value'),
        Input('applicant_income', 'value'),
        Input('coapplicant_income', 'value'),
        Input('loan_amount', 'value'),
        Input('loan_amount_term', 'value'),
        Input('credit_history', 'value'),
        Input('property_area', 'value')]
)
def update_output(n_clicks, gender, married, dependents, education, self_employed,
                    applicant_income, coapplicant_income, loan_amount, loan_amount_term,
                    credit_history, property_area):
    if n_clicks > 0:
        # Prepare input data for prediction
        input_data = pd.DataFrame({
            'Gender': [gender],
            'Married': [married],
            'Dependents': [dependents],
            'Education': [education],
            'Self_Employed': [self_employed],
            'Applicant_Income': [applicant_income],
            'Coapplicant_Income': [coapplicant_income],
            'Loan_Amount': [loan_amount],
            'Loan_Amount_Term': [loan_amount_term],
            'Credit_History': [credit_history],
            'Property_Area': [property_area]
        })
        # One-hot encode categorical variables
        input_data = pd.get_dummies(input_data)
 
        # Make predictions
        prediction = model.predict(input_data)
        if prediction[0] == 1:
            return html.Div('Loan Approved', style={'color': 'green'})
        else:
            return html.Div('Loan Rejected', style={'color': 'red'})
 
 
#Run the App
if __name__ == '__main__':
    app.run_server(debug=True)

