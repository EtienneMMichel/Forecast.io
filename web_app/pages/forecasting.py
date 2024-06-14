import dash
from dash import html, dcc, callback, Output, Input
from pages.utils import CONTENT_STYLE, SYMBOLS, TIMEFRAMES, MODELS
from pages.utils.api_call import get_data, predict
import plotly.graph_objects as go
import pandas as pd
from pages.utils.timestamp import get_next_timestamp

dash.register_page(__name__)







layout = html.Div([
    html.H1('Forecasting'),
    html.Div('This is our forecasting page!'),
    html.Div([
        html.H3('Forecasting'),
        dcc.Dropdown(SYMBOLS, SYMBOLS[0], id='symbol'),
        dcc.RadioItems(options=TIMEFRAMES, value=TIMEFRAMES[0], id='timeframe', inline=True),
        dcc.Slider(5, 20, 5,
               value=5,
               id='prediction_length'
        ),
        dcc.Dropdown(
                  id = "model",
                  options= MODELS,
                  multi=True),
        dcc.Graph(figure={}, id='controls-and-graph')
    ])
    
], style=CONTENT_STYLE)




@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    [Input(component_id='symbol', component_property='value'),
     Input(component_id='timeframe', component_property='value'),
     Input(component_id='model', component_property='value'),
     Input(component_id='prediction_length', component_property='value')]
)
def update_graph(symbol, timeframe, models, prediction_length):
    start_date = "2022-09-15"
    end_date = "2022-09-16"
    symbol_metadata = f"{symbol}_{timeframe}"

    df = pd.DataFrame.from_records(get_data([symbol_metadata], start_date, end_date)[symbol_metadata])
    closes = df['close'].to_numpy().reshape(-1,1).tolist()
    current_timestamp = df.loc[df.shape[0] - 1:, 'time'].values[0]
    next_timestamp = get_next_timestamp(current_timestamp, timeframe, prediction_length)
    nan_list = [None for _ in range(prediction_length)]
    df = pd.concat([df, pd.DataFrame({'time': next_timestamp, 'open': nan_list, 'high': nan_list, 'low': nan_list, 'close': nan_list})], ignore_index=True)
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(template="plotly_dark")

    # Add the prediction line
    if models:
        for model in models:
            prediction = predict(closes, model, [0], prediction_length)
            print(prediction)
            fig.add_trace(go.Scatter(x=next_timestamp, y=prediction,
                            mode='lines+markers',
                            name=model))
    return fig