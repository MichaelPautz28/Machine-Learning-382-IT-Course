import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import joblib

model = joblib.load('./artifacts/model_1.pkl')
df = pd.read_csv('./artifacts/feature_importance.csv', index_col=0)

features = df.index.tolist()
importance = df.iloc[:, 0].tolist()
#Initialise the Dash App
app = dash.Dash(__name__)
server = app.server
 
#Define App Layout
app.layout = html.Div(
    children=[
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
        dcc.Slider(
            id='income-slider',
            min=0,
            max=50000,
            step=100,
            value=5000,
            marks={i: f'${i}' for i in range(0, 50001, 5000)},
            tooltip={"always_visible":True}
        ),
        html.Label("Coapplicant Income:"),
        dcc.Slider(
            id='coincome-slider',
            min=0,
            max=50000,
            step=100,
            value=1000,
            marks={i: f'${i}' for i in range(0, 50001, 5000)},
            tooltip={"always_visible":True}
        ),
        html.Label("Loan Amount:"),
        dcc.Slider(
            id='loan-slider',
            min=0,
            max=1000,
            step=10,
            value=100,
            marks={i: f'${i}' for i in range(0, 1001, 100)}
        ),
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
        html.Div(id='output'),
        dcc.Graph(id='graph')
    ]
)
 
 
# Define Callback Function for Predictions
@app.callback(
    Output(component_id='output', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    [Input(component_id='gender', component_property='value'),
        Input(component_id='married', component_property='value'),
        Input(component_id='dependents', component_property='value'),
        Input(component_id='education', component_property='value'),
        Input(component_id='self_employed', component_property='value'),
        Input(component_id='income-slider', component_property='value'),
        Input(component_id='coincome-slider', component_property='value'),
        Input(component_id='loan-slider', component_property='value'),
        Input(component_id='loan_amount_term', component_property='value'),
        Input(component_id='credit_history', component_property='value'),
        Input(component_id='property_area', component_property='value')]
)
def update_output(n_clicks, gender, married, dependents, education, self_employed,
                    applicant_income, coapplicant_income, loan_amount, loan_amount_term,
                    credit_history, property_area):
    if not(n_clicks is None):
        # Prepare input data for prediction
        input_data = pd.DataFrame({
            'gender': [gender],
            'married': [married],
            'dependents': [dependents],
            'education': [education],
            'self_employed': [self_employed],
            'applicant_income': [applicant_income],
            'coapplicant_income': [coapplicant_income],
            'loan_amount': [loan_amount],
            'loan_amount_term': [loan_amount_term],
            'credit_history': [credit_history],
            'property_area': [property_area]
        }) 
        # Make predictions
        prediction = model.predict(input_data)
        if prediction == 1:
            return html.Div('Loan Approved', style={'color': 'green'})
        else:
            return html.Div('Loan Rejected', style={'color': 'red'})

# Define callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('graph', 'id')]
)
def update_graph(_):
    # Create horizontal bar graph
    fig = {
        'data': [
            {
                'x': importance,
                'y': features,
                'type': 'bar',
                'orientation': 'h'
            }
        ],
        'layout': {
            'title': 'Feature Importance',
            'xaxis': {'title': 'Importance'},
            'yaxis': {'title': 'Feature'},
        }
    }
    return fig
#Run the App
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)