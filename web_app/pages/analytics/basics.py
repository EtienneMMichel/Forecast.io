import dash
from dash import html
from pages.utils import CONTENT_STYLE


dash.register_page(__name__)

layout = html.Div([
    html.H1('Behind the data: understand the basics of analytics'),

    html.Div([])
], style=CONTENT_STYLE)