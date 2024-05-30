import dash
from dash import html
from pages.utils import CONTENT_STYLE
import dash_bootstrap_components as dbc
from pages.utils import get_pages, get_analytics_pages



dash.register_page(__name__)




layout = html.Div([
    html.H1('Analytics'),
    html.Div('This is the analytics page!'),

    html.Div(dbc.Nav(
    [
        dbc.NavLink(f"{page['name']} - {page['path']}", href=page["relative_path"])
        for page in list(filter(get_analytics_pages,get_pages()))
    ]
))
], style=CONTENT_STYLE)