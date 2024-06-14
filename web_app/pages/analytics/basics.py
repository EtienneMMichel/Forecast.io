import dash
from dash import html, dcc
from pages.utils import CONTENT_STYLE


dash.register_page(__name__)

layout = html.Div([
    html.Div([
        dcc.Markdown('''
        
        '''),
    ])
], style=CONTENT_STYLE)