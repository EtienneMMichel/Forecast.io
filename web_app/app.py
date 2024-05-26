import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from pages.utils import SIDEBAR_STYLE

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)



# the styles for the main content position it to the right of the sidebar and
# add some padding.




# content = html.Div(id="page-content", style=CONTENT_STYLE)

sidebar = html.Div(
    [
        html.A(html.H2("Sidebar", className="display-4"), href="/", style={"text-decoration": "none"}),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink(f"{page['name']}", href=page["relative_path"], active="exact")
            for page in list(filter(lambda page: page['path'] != "/", list(dash.page_registry.values())))],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([ dash.page_container,sidebar])

if __name__ == '__main__':
    app.run(debug=True)