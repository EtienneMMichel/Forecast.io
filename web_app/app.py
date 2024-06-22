import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State

from pages.utils import SIDEBAR_STYLE
from pages.utils import set_pages

app = dash.Dash(
                external_stylesheets=[dbc.themes.DARKLY],
                use_pages=True,
                prevent_initial_callbacks=True,
                suppress_callback_exceptions=True,
                update_title=None,
                title='Forecast.io')


# the styles for the main content position it to the right of the sidebar and
# add some padding.




# content = html.Div(id="page-content", style=CONTENT_STYLE)
offcanvas = html.Div(
    [
        dbc.Button("Menu",className="rounded-pill",outline=True, color="warning", id="open-offcanvas", n_clicks=0, style={"position": "sticky", "top":0}),
        dbc.Offcanvas(
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
                        dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            id="offcanvas",
            is_open=False,
        ),
    ]
)

frontpage = html.Div([offcanvas]) # add profil

app.layout = html.Div([
    html.Div(dash.page_container, style={"position": "relative"}),
    html.Div(frontpage, style={"position": "fixed","zIndex":2, "top":10, "left":10}),
    ], style={
        "background-color": "#492100",
        "background-image": "linear-gradient( 85.2deg,  rgba(33,3,40,1) 7.5%, rgba(65,5,72,1) 88.7% )"

    })

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open





if __name__ == '__main__':
    # set_pages(list(dash.page_registry.values()))
    app.run(debug=True)
    