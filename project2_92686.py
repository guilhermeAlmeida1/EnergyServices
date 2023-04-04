from dash import Dash, dcc, html, Input, Output
from itertools import combinations
import pandas as pd


gitRepoV0_0_0 = 'https://raw.githubusercontent.com/guilhermeAlmeida1/EnergyServices/fed1eea955e91f6225ee596cab001469986e4442'
assets = f'{gitRepoV0_0_0}/assets'

df_metrics= pd.read_csv(f'{assets}/metrics.csv').set_index('index')

comb = list()
vars = [0,1,2,3,4,5,6,7,8,9,10,11]
for i in range(6,len(vars)+1) :
    comb += list(combinations(vars, i))

combIndex = 0
prediction_svg = '{assets}/prediction{combIndex}.svg'
scatter_svg = '{assets}/scatter{combIndex}.svg'

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

header = '''
## This project projects power consumption at a given hour using Support Vector Regression.

It allows you to seamlessly test up between 2510 different combinations of input parameters.
Some additional plots are shown at the bottom to give a simple insight into data exploration and feature selection. 

By testing models with a few different inputs, you might come to the realisation that the 'Power-n' parameters have a very strong weight,
given that the model is able to predict with high accuracy with these parameters regardless of choosing others.
This comes to show that, despite being much simpler, an AutoRegression is already capable of modelling power consumption well, and the additional features have a lower relative importance.
'''

middletext = '''
\
\
\
\
\
### Scatter plots between Power Consumption and each feature.
'''

def getMetrics(idx):
    R2 = df_metrics.at[idx, 'R2']
    MAE = df_metrics.at[idx, 'MAE']
    MBE = df_metrics.at[idx, 'MBE']
    MSE = df_metrics.at[idx, 'MSE']
    RMSE = df_metrics.at[idx, 'RMSE']
    cvRMSE = df_metrics.at[idx, 'cvRMSE']
    NMBE = df_metrics.at[idx, 'NMBE']
    return f'\n\n\n\n\nR2:     {R2}\nMAE:    {MAE}\nMBE:    {MBE}\nMSE:    {MSE}\nRMSE:   {RMSE}\ncvRMSE: {cvRMSE}\nNMBE:   {NMBE}'


app = Dash(__name__)
app.layout = html.Div(children=[
        html.Div(children=[dcc.Markdown(children=header)], style={'width': '60%'}),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                html.Label(id='label_checklist', children='Select the desired features:'),
                dcc.Checklist(id='var_checklist',
                        options={0:'Temperature (ºC)', 1:'Humidity (%)', 2:'Wind speed (m/s)', 3:'Wind gust (m/s)', 4:'Solar radiation (W/m^2)', 5:'Hour of day', 6:'No work day', 7:'Power[t-1] (kWh)', 8:'Power[t-2] (kWh)', 9:'Power[t-3] (kWh)', 10:'Power[t-4] (kWh)', 11:'Power[t-5] (kWh)'},
                        value=['0','1','2','3','4','5','6','7','8','9','10','11'], style={'width': '33%'}
                ),
                ]),
            ], style={'display': 'inline', 'width': '60%', 'flex':1}),
            html.Div(id='metrics', children=[getMetrics(combIndex)], style={'white-space': 'pre-line', 'flex':1}),
        ], style={'width': '100%', 'display': 'flex', 'flex-direction': 'row'}),

        
        html.Div(children=[
            html.Div(children=[
                html.Label('Predicted energy consumption and real energy consumption', style={'horizontal-align': 'middle'}),
                html.Img(id='prediction_plot', src=f'{assets}/prediction{combIndex}.svg')
            ], style={'width': '60%', 'flex':1}),
            html.Div(children=[
                html.Label('Scatter plot of predicted/real energy consumption', style={'horizontal-align': 'middle'}),
                html.Img(id='scatter_plot', src=f'{assets}/scatter{combIndex}.svg')
            ], style={'width': '40%', 'flex':1}),
        ], style={'width': '100%', 'display': 'flex', 'flex-direction': 'row'}),
        
        html.Div(children=[dcc.Markdown(middletext)], style={'width': '60%'}),
        html.Img(id='vars', src=f'{assets}/params_scatter_plots.svg', width='100%')
    ], style={'width': '100%', 'display': 'inline', 'flex-direction': 'row', 'vertical-align': 'middle'})

@app.callback(
    Output(component_id='label_checklist', component_property='children'),
    Output(component_id='prediction_plot', component_property='src'),
    Output(component_id='scatter_plot', component_property='src'),
    Output(component_id='metrics', component_property='children'),
    Input(component_id='var_checklist', component_property='value'),
)
def callback_a(x):
    inputlist = list([int(numeric_string) for numeric_string in x])
    inputlist.sort()
    if (len(inputlist) < 6):
        return '! Please select at least 6 features.', f'{assets}/prediction0.svg', f'{assets}/scatter0.svg', getMetrics(0)
    else:
        combIndex = comb.index(tuple(inputlist))
        prediction_svg = f'{assets}/prediction{combIndex}.svg'
        scatter_svg = f'{assets}/scatter{combIndex}.svg'
        return 'Select the desired features:', prediction_svg, scatter_svg, getMetrics(combIndex)

if __name__ == '__main__':
    app.run_server(debug=False)