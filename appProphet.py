from flask import Flask
import config
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os
import pandas as pd
pd.options.mode.chained_assignment = None # avoid warning of replacing data
import plotly.express as px
import plotly.graph_objects as go
import forecasting as fordat

def create_line_plot(data):
    # sub_data = data[data['Cadena 2020'] == cadena]
    # grp = data.groupby(by=['Sector', 'Year'])['FOBDOL'].sum().reset_index()
    grp = data.groupby(by=['Sector', 'Year_month'])['FOBDOL'].sum().reset_index()
    lineplt = px.line(grp, x='Year_month', y='FOBDOL', color='Sector',
            title='Serie de tiempo Anual por sector')
    return lineplt

def filter_df(data, key, value):
    sub_data = data[data[key] == value]
    return sub_data

def create_forecast_plot(db, sector, pais):

    test, predictions = fordat.forecast_prophet(db[sector])

    fig = go.Figure()
    test_df = test.reset_index(name='test')

    history = db[sector][-24:].reset_index(name='history')
    print(history)
    fig.add_trace(go.Scatter(y=history['history'],
                             x=history['Year_month'],
                             mode='lines+markers',
                             name='history'))

    fig.add_trace(go.Scatter(y=test_df['test'],
                             x=test_df['Year_month'],
                             mode='lines+markers',
                             name='test'))
    dates = pd.date_range(test.index.min(), periods=len(test) + 12, freq='MS')

    fig.add_trace(go.Scatter(y=predictions,
                             x= dates,
                              mode='lines',
                              name='predictions'))

    fig.update_layout(
        title=f"Prediccion ultimos meses {sector} en {pais}",
        xaxis_title="Months",
        yaxis_title="FOBDOL",
        # xaxis_tickformat='%d %B (%a)<br>%Y',
        legend_title="Data")

    return fig


#external_stylesheets = [os.path.join('boostrap.css')]

workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name
request_path_prefix = None
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'


## server configurations
server = Flask( config.app_name )
app = dash.Dash( config.app_name, external_stylesheets=[dbc.themes.COSMO] , server=server)


#from google.colab import drive
#drive.mount('/content/drive',  force_remount=True)
#folder_route = "/content/drive/MyDrive/Ds4 Computer Science/Procolombia project/data/"
#df = pd.read_pickle(folder_route + "base_datos_corregida.pkl")

df = pd.read_pickle(os.path.join('base_datos_corregida.pkl'))

filteredData = df[["Cadena 2020","Sector 2020","Subsector 2020","FOBDOL","Year_month","COD_PAI4","Destination country","RAZ_SIAL"]]
filteredData.dropna(inplace=True)
filteredData.columns = ["Cadena","Sector","Subsector","FOBDOL","Year_month","CodeCountry","Country","Empresa"]
# transforming date in due format
filteredData["Date"] = pd.to_datetime(filteredData["Year_month"], format="%Y-%m-%d")
filteredData['Year'] = filteredData.Date.dt.year

# getting all options for dropdown lists
available_Cadenas = filteredData['Cadena'].unique()
sector_options = [list(filteredData[filteredData["Cadena"] == cadena]["Sector"].unique()) for cadena in available_Cadenas]
subsectors_options = []
for i in range(len(sector_options)):
    subsectors_options.append({sector: list(filteredData[filteredData["Sector"] == sector]['Subsector'].unique()) for sector in sector_options[i]})
# zipping lists of cadenas, sectors, and subsectors
all_options = dict(zip(available_Cadenas,subsectors_options))
all_countries = filteredData["Country"].unique()

## Create lineplot for user
sub_data = filter_df(filteredData, 'Cadena', available_Cadenas[0])
sub_data = filter_df(sub_data, 'Country', all_countries[0])
lineplot = create_line_plot(sub_data)

app.layout = html.Div([
    html.Div([html.H1('FORDAT: forecasting tool'),
              html.Hr(),
              ]),
    html.Div(
    [
        dcc.Dropdown( id='cadenas-dropdown', placeholder='Seleccione cadena',
                     options=[{'label': k, 'value': k} for k in all_options.keys()],
                    value='Agroalimentos'),
        dcc.Dropdown(id='sectors-dropdown', placeholder='Selecione sector'),
        dcc.Dropdown(id='subsectors-dropdown', placeholder='Selecione subsector'),
        dcc.Dropdown(id='country-dropdown', value=all_countries[0], placeholder='Selecione pais')
        ],   style={ "width": "50%"},
    ),

    html.Hr(),

    html.Div([
        dcc.Tabs(id="tabs-selection", value='tab-1', children=[
            dcc.Tab(label='EDA', value='tab-1'),
            dcc.Tab(label='Forecasting', value='tab-2'),
        ], colors={
            "border": "white",
            "primary": "gold",
            "background": "cornsilk"
        }),
        html.Div(id='tabs-div')
    ])
])

eda_div =  html.Div([
        dcc.Graph(id='map-plot'),#,  style={'display': 'inline-block'}),
        dcc.Graph(id='line-plot')#,  style={'display': 'inline-block'}),
    ])

forecast_div = html.Div([
        html.H2('Forecasting plot', id='forecast-title'),
        html.Button('Make forecast', id='forecast-button', n_clicks=0),
        # dcc.Slider(id='future-months',
        #            min=1,
        #            max=60,
        #            value=1,
        #            step=None),
        dcc.Loading(
            id="loading-2",
            children=[html.Div([dcc.Graph(id='forecast-plot')])],
            type="circle",
        )
    ])


@app.callback(Output('tabs-div', 'children'),
              Input('tabs-selection', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return eda_div
    elif tab == 'tab-2':
        return forecast_div

@app.callback(Output('forecast-title', 'children'),
    [Input('cadenas-dropdown', 'value'),
     Input('sectors-dropdown', 'value'),
     # Input('subsectors-dropdown', 'value'),
     Input('country-dropdown','value')])
def update_forecast_title(cadena, sector, country):
    if country == None:
        country = 'Global'
    return f'Prediccion de {sector} en {country}. Cadena: {cadena}'

## Update forecast graph
@app.callback(
    Output(component_id='forecast-plot', component_property='figure'),
    [Input(component_id='forecast-button', component_property='n_clicks')],
    [State(component_id='sectors-dropdown', component_property='value'),
    State(component_id='cadenas-dropdown', component_property='value'),
    State(component_id='country-dropdown', component_property='value')]
)
def update_forecast_div(n_clicks, sector, cadena, pais):
    sub_data = filter_df(filteredData, 'Cadena', cadena)
    if not pais == None:
        sub_data = filter_df(sub_data, 'Country', pais)
    db = sub_data.groupby(by=['Sector', 'Year_month'])['FOBDOL'].sum().unstack(0)

    forecast_plot = create_forecast_plot(db, sector, pais)
    return forecast_plot


@app.callback(Output('line-plot', 'figure'),
              [Input('cadenas-dropdown', 'value'),
                Input('country-dropdown','value'),
              ])
def update_lineplot_div(cadena, pais):
    sub_data = filter_df(filteredData, 'Cadena', cadena)
    sub_data = filter_df(sub_data, 'Country', pais)
    plot = create_line_plot(sub_data)
    return plot

@app.callback(Output('map-plot', 'figure'),
    [Input('cadenas-dropdown', 'value'),
     Input('sectors-dropdown', 'value'),
     Input('subsectors-dropdown', 'value')])
def update_figure(selected_cadena, selected_sector, selected_subsector):
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


### Update dropdowns options and values callbakcs

@app.callback(
    dash.dependencies.Output('country-dropdown', 'options'),
    [dash.dependencies.Input('subsectors-dropdown', 'value')])
def set_cities_options(subsector):
    all_countries = filteredData[filteredData['Subsector']==subsector]['Country'].unique()
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


print("READY")

##############################

if __name__ == "__main__":
    
    app.run_server(host=config.app_host , port=config.app_port, debug=True)#config.app_debug)
