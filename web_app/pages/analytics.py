import dash
from dash import html
from pages.utils import CONTENT_STYLE


dash.register_page(__name__)

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
], style=CONTENT_STYLE)