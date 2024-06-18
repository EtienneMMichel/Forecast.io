import dash
from dash import html, dcc,  callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm



from .utils import CONTENT_STYLE, SYMBOLS, TIMEFRAMES, DATA_TYPE, api_call

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

ADF_card = dbc.Card(
    [
        dbc.CardBody(
                        [
                            html.H4("ADF Test", className="card-title"),
                            
                            html.P(
                                "This is a wider card with supporting text "
                                "below as a natural lead-in to additional "
                                "content. This content is a bit longer.",
                                className="card-text",
                            ),
                            dbc.Row([
                                dbc.Label("p-value"),
                                dbc.Progress(id='ADF-p-value', className="p-0"),
                                # dbc.Label("ADF-stat"),
                                # dbc.Progress(id='ADF-stat', className="p-0"),
                            ]),
                            html.Small(
                                "Last updated 3 mins ago",
                                className="card-text text-muted",
                            ),
                        ]
                    )
    ],
)

KPSS_card = dbc.Card(
    [
        dbc.CardBody(
                        [
                            html.H4("KPSS Test", className="card-title"),
                            
                            html.P(
                                "This is a wider card with supporting text "
                                "below as a natural lead-in to additional "
                                "content. This content is a bit longer.",
                                className="card-text",
                            ),
                            dbc.Row([
                                dbc.Label("p-value"),
                                dbc.Progress(id='KPSS-p-value', className="p-0"),
                                # dbc.Label("KPSS-stat"),
                                # dbc.Progress(id='KPSS-stat', className="p-0"),
                            ]),
                            html.Small(
                                "Last updated 3 mins ago",
                                className="card-text text-muted",
                            ),
                        ]
                    )
    ],
)

stationnarity = html.Div([
                    dbc.Row(dbc.Col(html.H3('Stationnarity'))),
                    dbc.Row(dbc.Col(html.P("Stationarity is an important property of time series data that indicates that the statistical properties of the data do not change over time"))),
                    dbc.Row([
                        dbc.Col(ADF_card, className="col-md-6"),
                        dbc.Col(KPSS_card, className="col-md-6")
                    ])
                ])

heavy_tails = html.Div([
                    dbc.Row(dbc.Col(html.H3('Heavy tails distributions'))),
                    dbc.Row(dbc.Col(html.P("Heavy tails distributions are distributions that have a higher probability of extreme events than the normal distribution. This can be a problem for forecasting because the model will not be able to predict these events."))),
                    dcc.Graph(id='heavy_tails_graph'),
                    # show comparaision between returns and normal distribution
                ])


symbol_selection = dbc.Row(
    [
        dbc.Label("Symbol", width=2),
        dcc.Dropdown(SYMBOLS, SYMBOLS[0], id='symbol_selection'),
    ],
    className="mb-3",
)

timeframe_selection = dbc.Row(
    [
        dbc.Label("Timeframe", width=2),
        dcc.RadioItems(options=TIMEFRAMES, value=TIMEFRAMES[0], id='timeframe_selection', inline=True),
    ],
    className="mb-3",
)

type_data = dbc.Row(
    [
        dbc.Label("Radios", html_for="example-radios-row", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="dataType",
                options=[{"label":type_, "value":i} for i, type_ in enumerate(DATA_TYPE)],
                value=0
            ),
            width=10,
        ),
    ],
    className="mb-3",
)


data_selection = dbc.Form([symbol_selection,timeframe_selection, type_data])

symbol_description = dbc.Card([
    dbc.CardHeader("Card header", className="bg-transparent"),
    dbc.CardBody(
        [
            html.H4("Symbol Description", className="card-title"),
            html.P(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum "
            )
        ]
        
    )], className="bg-transparent", color="success", outline=True)


layout = html.Div([
            dbc.Container(html.Div([
                    dbc.Row(dbc.Col(html.H1('Analytics'))),
                    dbc.Row(dbc.Col(html.P('This is the analytics page! Here you can analyse easily data you want to proceed.'))),
                    dbc.Row(dbc.Col(introduction)),
                    dbc.Row([dbc.Col(data_selection), dbc.Col(symbol_description)], className="mb-3"),
                    dbc.Row(dcc.Graph(id='plot_data')),
                    dcc.Store(id='returns_data'),

                    stationnarity,
                    heavy_tails,
                    ## Gain/loss asymmetry
                    ## Aggregationnal Gaussianity: for lower frequencies, the distribution tends to become more Gaussian
                    ## Volatility clustering  
                ]), fluid=True)
            ], style=CONTENT_STYLE)



#============================CALLBACKS===================================================================

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
    return df.to_dict(orient="records")


@callback(Output('heavy_tails_graph', 'figure'), [Input('returns_data', 'data'), Input('dataType','value')])
def get_heavy_tails_graph(jsonified_cleaned_data, data_type):
    x_inf = -0.006
    x_sup = 0.006
    df = pd.DataFrame.from_records(jsonified_cleaned_data)
    if DATA_TYPE[data_type].split('_')[-1] == 'returns':
        data = df[DATA_TYPE[data_type]].loc[1:].to_numpy()
    else:
        data = df['close_returns'].loc[1:].to_numpy()
    
    # fig = ff.create_distplot([gaussian_dist_sample], ["gaussian distribution"], show_hist=False)
    fig = px.histogram(data, range_x=[x_inf, x_sup])
    
    x_axis = np.linspace(x_inf, x_sup, 500)
    pdf_gaussian = norm.pdf(x_axis, data.mean(), data.std()) # why /2 ???????? sorry about that comment
    fig.add_trace(go.Scatter(x=x_axis, y=pdf_gaussian,
                    mode='lines',
                    name='Gaussian distribution'))
    fig.update_layout(template="plotly_dark")
    return fig


@callback([Output('ADF-p-value', 'value'), Output("ADF-p-value", "label"), Output("ADF-p-value", "color"),
        #    Output('ADF-stat', 'value'), Output("ADF-stat", "label"), Output("ADF-stat", "color"),
           Output('KPSS-p-value', 'value'), Output("KPSS-p-value", "label"), Output("KPSS-p-value", "color"),
        #    Output('KPSS-stat', 'value'), Output("KPSS-stat", "label"), Output("KPSS-stat", "color"),
           ],
           
           [Input('returns_data', 'data'), Input('dataType','value')])
def get_stationnarity(jsonified_cleaned_data, data_type):
    df = pd.DataFrame.from_records(jsonified_cleaned_data)
    data = df[DATA_TYPE[data_type]].loc[1:].to_numpy()
    inputs = {
        "values": data.tolist()
    }
    response = api_call.get_stationnarity(inputs)
    adf = response["ADF"]
    kpss = response["KPSS"]
    adf_p_value_color = "success" if adf["p-value"] < 0.05 else "danger"
    adf_stat_color = "success" if adf["ADF-stat"] < 0.05 else "danger"
    kpss_p_value_color = "success" if kpss["p-value"] > 0.05 else "danger"
    kpss_stat_color = "success" if kpss["KPSS-stat"] < 0.05 else "danger"
    return (1 - adf["p-value"])*100, str(adf["p-value"]), adf_p_value_color, (1 - kpss["p-value"])*100,str(kpss["p-value"]), kpss_p_value_color


@callback(Output('plot_data', 'figure'), [Input('returns_data', 'data'), Input('dataType','value')])
def plot_data(jsonified_cleaned_data, data_type):
    df = pd.DataFrame.from_records(jsonified_cleaned_data)
    fig = px.line(df, x="time", y=DATA_TYPE[data_type], title=f"{DATA_TYPE[data_type]}")
    fig.update_layout(template="plotly_dark")
    return fig