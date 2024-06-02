import dash
from dash import html, dcc, callback, Output, Input
from pages.utils import CONTENT_STYLE
from api_call import get_data, predict
import plotly.graph_objects as go
import pandas as pd
from pages.utils.timestamp import get_next_timestamp

dash.register_page(__name__)







layout = html.Div([
    html.H1('Forecasting'),
    html.Div('This is our forecasting page!'),
    html.Div([
        html.H3('Forecasting'),
        dcc.RadioItems(options=['EURCHF', 'EURJPY'], value='EURCHF', id='symbol'),
        dcc.RadioItems(options=['H1'], value='H1', id='timeframe'),
        dcc.RadioItems(options=['LinearReg'], value='LinearReg', id='model'),
        dcc.Graph(figure={}, id='controls-and-graph')
    ])
    
], style=CONTENT_STYLE)




@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    [Input(component_id='symbol', component_property='value'),
     Input(component_id='timeframe', component_property='value'),
     Input(component_id='model', component_property='value')]
)
def update_graph(symbol, timeframe, model):
    start_date = "2022-09-15"
    end_date = "2022-09-16"
    symbol_metadata = f"{symbol}_{timeframe}"
    df = pd.DataFrame.from_records(get_data([symbol_metadata], start_date, end_date)[symbol_metadata])
    closes = df['close'].to_numpy().reshape(-1,1).tolist()
    prediction = predict(closes, model, [0], 5)
    current_timestamp = df.loc[df.shape[0] - 1:, 'time'].values[0]
    next_timestamp = get_next_timestamp(current_timestamp, timeframe, prediction)
    nan_list = [None for _ in range(len(prediction))]
    df = pd.concat([df, pd.DataFrame({'time': next_timestamp, 'open': nan_list, 'high': nan_list, 'low': nan_list, 'close': nan_list})], ignore_index=True)
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(template="plotly_dark")
    fig.add_trace(go.Scatter(x=next_timestamp, y=prediction,
                    mode='lines+markers',
                    name=model))
    return fig