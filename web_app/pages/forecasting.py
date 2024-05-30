import dash
from dash import html
from pages.utils import CONTENT_STYLE


dash.register_page(__name__)

layout = html.Div([
    html.H1('Forecasting'),
    html.Div('This is our forecasting page!'),
], style=CONTENT_STYLE)