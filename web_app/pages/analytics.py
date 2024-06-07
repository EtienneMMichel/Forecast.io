import dash
from dash import html, dcc,  callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm

from .utils import CONTENT_STYLE, SYMBOLS, TIMEFRAMES, api_call

dash.register_page(__name__)

introduction = dbc.Alert(
    [
        html.H4("Introduction", className="alert-heading"),
        html.P(
            "When you do forecasting, you use models which are built upon hypothesis on your data. "
            "The more they follows your hypothesis and more your model will be accurate. "
        ),
        html.Hr(),
        html.P(
            "Usually, you have two main solutions. The first one is to adapt your model to lightweight the hypothesis "
            "and the other one is to trick your data to make them closer to the hypothesis.",
            className="mb-0",
        ),
    ]
)

stationnarity = html.Div([
                    dbc.Row(dbc.Col(html.H3('Stationnarity'))),
                    dbc.Row(dbc.Col(html.P("Stationarity is an important property of time series data that indicates that the statistical properties of the data do not change over time")))
                ])

heavy_tails = html.Div([
                    dbc.Row(dbc.Col(html.H3('Heavy tails distributions'))),
                    dbc.Row(dbc.Col(html.P("Stationarity is an important property of time series data that indicates that the statistical properties of the data do not change over time"))),
                    dcc.Graph(id='heavy_tails_graph'),
                    # show comparaision between returns and normal distribution
                ])

data_selection = html.Div([
                        dbc.Row(dbc.Col(dcc.Dropdown(SYMBOLS, SYMBOLS[0], id='symbol_selection'))),
                        dbc.Row(dbc.Col(dcc.RadioItems(options=TIMEFRAMES, value=TIMEFRAMES[0], id='timeframe_selection', inline=True)))
                    ])


layout = html.Div([
            dbc.Container(html.Div([
                    dbc.Row(dbc.Col(html.H1('Analytics'))),
                    dbc.Row(dbc.Col(html.P('This is the analytics page! Here you can analyse easily data you want to proceed.'))),
                    dbc.Row(dbc.Col(introduction)),
                    dbc.Row(dbc.Col(data_selection)),
                    dcc.Store(id='returns_data'),

                    stationnarity,
                    heavy_tails,
                    ## Gain/loss asymmetry
                    ## Aggregationnal Gaussianity: for lower frequencies, the distribution tends to become more Gaussian
                    ## Volatility clustering  
                ]), fluid=True)
            ], style=CONTENT_STYLE)


@callback(
    Output('returns_data', 'data'),
    [
        Input('symbol_selection', 'value'),
        Input('timeframe_selection', 'value'),
    ]
    )
def get_data(symbol, timeframe):
    start_date = "2020-01-01"
    end_date = "2022-01-01"
    symbol_metadata = f"{symbol}_{timeframe}"
    response = api_call.get_data([symbol_metadata], start_date, end_date)
    df = pd.DataFrame.from_records(response[symbol_metadata])
    df["close_returns"] = (df.close - df.close.shift(1))/df.close.shift(1)
    return df.to_dict(orient="records")


@callback(Output('heavy_tails_graph', 'figure'), [Input('returns_data', 'data')])
def get_heavy_tails_graph(jsonified_cleaned_data):
    x_inf = -0.006
    x_sup = 0.006
    df = pd.DataFrame.from_records(jsonified_cleaned_data)
    data = df['close_returns'].loc[1:].to_numpy()
    
    # fig = ff.create_distplot([gaussian_dist_sample], ["gaussian distribution"], show_hist=False)
    fig = px.histogram(data, range_x=[x_inf, x_sup])
    
    x_axis = np.linspace(x_inf, x_sup, 500)
    pdf_gaussian = norm.pdf(x_axis, data.mean(), data.std())/ 2 # why /2 ???????? sorry about that comment
    fig.add_trace(go.Scatter(x=x_axis, y=pdf_gaussian,
                    mode='lines',
                    name='Gaussian distribution'))
    fig.update_layout(template="plotly_dark")
    return fig