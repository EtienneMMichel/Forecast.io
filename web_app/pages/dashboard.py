import dash
from dash import html, dcc,  callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm



from .utils import CONTENT_STYLE, SYMBOLS, TIMEFRAMES, DATA_TYPE, api_call, MODELS
from .utils.timestamp import get_next_timestamp

dash.register_page(__name__)



#=========================== PRICE TAB =========================

#=========================== data selection ============================================================
symbol_selection = dbc.Row(
    [
        dbc.Label("Symbol"),
        dcc.Dropdown(SYMBOLS, SYMBOLS[0], id='price_symbol_selection'),
    ],
    className="mb-0",
)

timeframe_selection = dbc.Row(
    [
        dbc.Label("Timeframe"),
        dcc.RadioItems(options=TIMEFRAMES, value=TIMEFRAMES[0], id='price_timeframe_selection', inline=True),
    ],
    className="mb-0",
)

data_selection = dbc.Card([
                    dbc.CardHeader(html.H4("Data Selection")),
                    dbc.CardBody(dbc.Form([symbol_selection,timeframe_selection]), className="card-text")
                ])



#=========================== DATA ANALYSIS ============================================================
data_analysis = dbc.Card([
                    dbc.CardHeader(html.H4("Data Analysis")),
                    dbc.CardBody(html.Div([
                        dbc.Row([
                            dbc.Col(
                                dcc.Dropdown(
                                    id = "cause_symbols",
                                    options= SYMBOLS,
                                    value=SYMBOLS[:1],
                                    multi=True),
                                className="col-md-4"
                            ),
                            dbc.Col(
                                dcc.Graph(id='causality_plot_data'),
                                className="col-md-8"
                            )
                        ])
                    ]), className="card-text")
                ])

# ========================= FORECASTING =================================================

forecasting = html.Div([
        dcc.Slider(5, 20, 5,
               value=5,
               id='price_prediction_length'),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='price_plot_data'),
                className="col-md-8"
            ),
            dbc.Col(
                dcc.Dropdown(
                    id = "price_model",
                    options= MODELS,
                    multi=True),
                className="col-md-4"
            )
        ])
    ])


content_price_tab = dbc.Container([
            dbc.Row([
                dbc.Col(data_selection, className="col-md-4"),
                dbc.Col(data_analysis, className="col-md-8")
            ], className="mb-3"),
            dcc.Store(id='price_data'),
            forecasting
        ],fluid=True)











content_spread_tab = html.P('This is ffffan analyse easily data you want to proceed.')

card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Price", tab_id="price-tab"),
                    dbc.Tab(label="Spread", tab_id="spread-tab"),
                ],
                id="card-tabs",
                active_tab="price-tab",
            ),
            className="bg-transparent"
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)

layout = html.Div([
            dbc.Container(html.Div([
                    dbc.Row(dbc.Col(html.H1('Dashboard'))),
                    dbc.Row(dbc.Col(html.P('This is the analytics page! Here you can analyse easily data you want to proceed.'))),
                    card 
                ]), fluid=True)
            ], style=CONTENT_STYLE)



#============================CALLBACKS===================================================================

@callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "price-tab":
        return content_price_tab
    if active_tab == "spread-tab":
        return content_spread_tab
    

@callback(
    Output('price_data', 'data'),
    [
        Input('price_symbol_selection', 'value'),
        Input('price_timeframe_selection', 'value'),
    ]
    )
def price_get_data(symbol, timeframe):
    start_date = "2022-09-15"
    end_date = "2022-09-16"
    symbol_metadata = f"{symbol}_{timeframe}"
    response = api_call.get_data([symbol_metadata], start_date, end_date)
    df = pd.DataFrame.from_records(response[symbol_metadata])
    return df.to_dict(orient="records")
    





@callback(
    Output(component_id='price_plot_data', component_property='figure'),
    [Input('price_data', 'data'),
     Input('price_timeframe_selection', 'value'),
     Input(component_id='price_model', component_property='value'),
     Input(component_id='price_prediction_length', component_property='value')]
)
def update_graph(jsonified_cleaned_data, timeframe, models, prediction_length):
    print("prediction_length: ", prediction_length)
    df = pd.DataFrame.from_records(jsonified_cleaned_data)
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
            prediction = api_call.predict(closes, model, [0], prediction_length)
            fig.add_trace(go.Scatter(x=next_timestamp, y=prediction,
                            mode='lines+markers',
                            name=model))
    return fig

    
@callback(
    Output(component_id='causality_plot_data', component_property='figure'),
    [
     Input('price_symbol_selection', 'value'),
     Input('cause_symbols', 'value'),
     Input(component_id='price_prediction_length', component_property='value')]
)
def update_graph(ref_symbol, cause_symbols, prediction_length):
    payload = {
        "ref_ticket": ref_symbol,
        "cause_tickets": cause_symbols,
        "start_date": "2020-10-01 00:00:00",
        "end_date": "2022-08-01 00:00:00",
        "period": "D20",
        "timeframe": "H1",
        "data_type": "close_returns",
        "max_lags": 1
        }
    response = api_call.get_granger_causality(payload)
    data = []
    for date, results in response.items():
        for cause_symbol, result in results.items():
            data.append({
                "date": date,
                "cause_symbol": cause_symbol,
                "p-value": result["1"]["ssr_chi2test"]["pvalue"]
            })
    df = pd.DataFrame.from_dict(data) 
    fig = px.line(df, x="date", y="p-value", color='cause_symbol')
    fig.update_layout(template="plotly_dark")
    fig.update_layout(yaxis_range=[0,1])
    return fig



