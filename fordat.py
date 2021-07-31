
from flask import Flask
import config
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
pd.options.mode.chained_assignment = None # avoid warning of replacing data

from fbprophet import Prophet
import dash_bootstrap_components as dbc
import os

import plotly.express as px
#import pycountry


## server configurations
server = Flask( config.app_name )
app = dash.Dash( config.app_name, external_stylesheets=[dbc.themes.BOOTSTRAP] , server=server)




## read dataframe
#from google.colab import drive
#drive.mount('/content/drive',  force_remount=True)

#folder_route = "/content/drive/MyDrive/Ds4 Computer Science/Procolombia project/data/"
#df = pd.read_pickle(folder_route + "base_datos_corregida.pkl")
print("loading base")
df = pd.read_pickle(os.path.join('base_datos_corregida.pkl'))
print("loaded base")

# getting useful data only
filteredData = df[["Cadena 2020","Sector 2020","Subsector_EN","FOBDOL","Year_month","COD_PAI4","Destination country","RAZ_SIAL"]]
filteredData.dropna(inplace=True)
filteredData.columns = ["Cadena","Sector","Subsector","FOBDOL","Date","CodeCountry","Country","Empresa"]
# transforming date in due format
filteredData["Date"] = pd.to_datetime(filteredData["Date"], format="%Y-%m-%d")
# getting all options for dropdown lists
available_Cadenas = filteredData['Cadena'].unique()
sector_options = [list(filteredData[filteredData["Cadena"] == cadena]["Sector"].unique()) for cadena in available_Cadenas]
subsectors_options = []
for i in range(len(sector_options)):
    subsectors_options.append({sector: list(filteredData[filteredData["Sector"] == sector]['Subsector'].unique()) for sector in sector_options[i]})
# zipping lists of cadenas, sectors, and subsectors
all_options = dict(zip(available_Cadenas,subsectors_options))

app.layout = html.Div([
    dcc.Dropdown(
        id='cadenas-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Agroalimentos'
    ),
    html.Hr(),
    dcc.Dropdown(id='sectors-dropdown'),
    html.Hr(),
    dcc.Dropdown(id='subsectors-dropdown'),
    html.Hr(),
    dcc.Dropdown(id='country-dropdown'),
    html.Hr(),
    html.Div(id='display-selected-values'),
    html.Hr(),
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(id='future-months',
                  min=1,
                  max=5,
                  value=1,
                  marks={1: '1',2: '2',3: '3',4: '4', 5: '5'},
                  step=None)
    ])
])

@app.callback(Output('graph-with-slider', 'figure'),
    [Input('cadenas-dropdown', 'value'),
     Input('sectors-dropdown', 'value'),
     Input('subsectors-dropdown', 'value'),
     Input('country-dropdown','value'),
     Input('future-months','value')])
def update_figure(selected_cadena, selected_sector, selected_subsector, selected_country, future_months):
    b_cadena = 'Cadena == "'+selected_cadena+'"'
    if (selected_sector == None):
        userInterest = (filteredData.filter(
            items=["Cadena", "FOBDOL","Date"]).query(b_cadena))
        #plot of the map
        my_df = (filteredData.filter(
             items=["Cadena", "FOBDOL","CodeCountry"]).query(b_cadena))
        my_df.drop(columns=["Cadena"], inplace = True)
    elif (selected_subsector == None):
        b_sector = 'Sector == "'+selected_sector+'"'
        userInterest = (filteredData.filter(
            items=["Cadena", "Sector", "FOBDOL", "Date"]).query(b_cadena).query(b_sector))
        #plot of the map
        my_df = (filteredData.filter(
             items=["Cadena", "Sector", "FOBDOL","CodeCountry"]).query(b_cadena).query(b_sector))
        my_df.drop(columns=["Cadena", "Sector"], inplace = True)
    else:
        b_sector = 'Sector == "'+selected_sector+'"'
        b_subsector = 'Subsector == "'+selected_subsector+'"'
        userInterest = (filteredData.filter(
            items=["Cadena", "Sector", "Subsector","FOBDOL","Date"]).query(b_cadena).query(b_sector).query(b_subsector))
        #plot of the map
        my_df = (filteredData.filter(
             items=["Cadena", "Sector", "Subsector","FOBDOL","CodeCountry"]).query(b_cadena).query(b_sector).query(b_subsector))
        my_df.drop(columns=["Cadena", "Sector", "Subsector"], inplace = True)
    
    country_exports = my_df.groupby([my_df["CodeCountry"]])["FOBDOL"].sum().reset_index()
    fig = px.scatter_geo(country_exports, locations="CodeCountry",size="FOBDOL")
    # fig.show()
    fig.update_layout(transition_duration=500)
    return fig
    #modelo for prediciton
    #data = userInterest[["FOBDOL","Date"]]
    #data.columns = ["y","ds"] # rename columns to the prophet library
    #m = Prophet(interval_width=0.95, seasonality_mode='multiplicative')
    #model = m.fit(data)
    #future = m.make_future_dataframe(periods=future_months, freq='MS')
    #forecast = m.predict(future)
    #fig = m.plot(forecast)
    #fig.update_layout(transition_duration=500)
    
@app.callback(
    dash.dependencies.Output('country-dropdown', 'options'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def set_cities_options(selected_country):
    all_countries = filteredData["Country"].unique()
    return [{'label': i, 'value': i} for i in all_countries]
    
@app.callback(
    dash.dependencies.Output('sectors-dropdown', 'options'),
    [dash.dependencies.Input('cadenas-dropdown', 'value')])
def set_cities_options(selected_cadena):
    return [{'label': i, 'value': i} for i in all_options[selected_cadena]]

@app.callback(
    dash.dependencies.Output('sectors-dropdown', 'value'),
    [dash.dependencies.Input('sectors-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('subsectors-dropdown', 'options'),
    [dash.dependencies.Input('cadenas-dropdown', 'value'),
     dash.dependencies.Input('sectors-dropdown', 'value')])
def set_landmarks_options(selected_cadena, selected_sector):
    return [{'label': i, 'value': i} for i in all_options[selected_cadena][selected_sector]]

@app.callback(
    dash.dependencies.Output('subsectors-dropdown', 'value'),
    [dash.dependencies.Input('subsectors-dropdown', 'options')])
def set_landmarks_value(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('cadenas-dropdown', 'value'),
     dash.dependencies.Input('sectors-dropdown', 'value'),
     dash.dependencies.Input('subsectors-dropdown', 'value'),
     dash.dependencies.Input('future-months','value')])
def set_display_children(selected_cadena, selected_sector, selected_subsector,future_months):
    future_months = int(future_months)*12
    return u'{} is in {} of {} prediction for {}'.format(
        selected_subsector, selected_sector, selected_cadena, future_months
    )





##############################33

if __name__ == "__main__":
    
    app.run_server(host=config.app_host , port=config.app_port, debug=config.app_debug)