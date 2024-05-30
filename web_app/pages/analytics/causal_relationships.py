import dash
from dash import html
from pages.utils import CONTENT_STYLE


dash.register_page(__name__)

layout = html.Div([
    html.H1('Networks of causal relationships in the U.S. stock market'),
    html.Div('source : https://doi.org/10.1515/demo-2022-0110'),

    html.Div([])
], style=CONTENT_STYLE)