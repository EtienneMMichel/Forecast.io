import dash
from dash import html, dcc, callback, Output, Input
from pages.utils import CONTENT_STYLE
from api_call import get_data
import plotly.graph_objects as go
import pandas as pd


dash.register_page(__name__)







layout = html.Div([
    html.H1('Forecasting'),
    html.Div('This is our forecasting page!'),
    dcc.RadioItems(options=['EURCHF_H1', 'EURJPY_H1'], value='EURCHF_H1', id='controls-and-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph')
], style=CONTENT_STYLE)


@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(symbol_metadata):
    start_date = "2020-09-18"
    end_date = "2022-09-16"
    df = pd.DataFrame.from_records(get_data([symbol_metadata], start_date, end_date)[symbol_metadata])
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(template="plotly_dark")
    return fig