import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from pages.utils import SIDEBAR_STYLE
from pages.utils import set_pages

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], use_pages=True, prevent_initial_callbacks=True)


# the styles for the main content position it to the right of the sidebar and
# add some padding.




# content = html.Div(id="page-content", style=CONTENT_STYLE)

sidebar = html.Div(
    [
        html.A(html.H2("Forecast.io", className="display-4"), href="/", style={"text-decoration": "none"}),
        html.Hr(),
        html.P(
            "Explore financial word with ease", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Forecasting", href="/forecasting", active="exact"),
                dbc.NavLink("Analytics", href="/analytics", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([ dash.page_container,sidebar])

if __name__ == '__main__':
    # set_pages(list(dash.page_registry.values()))
    app.run(debug=True)
    