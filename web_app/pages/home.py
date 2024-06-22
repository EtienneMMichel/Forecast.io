import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')

'''
<div
  class="bg-image"
  style="
    background-image: url('https://mdbcdn.b-cdn.net/img/new/fluid/nature/012.webp');
    height: 100vh;
  "
>
  <div class="mask" style="background-color: rgba(0, 0, 0, 0.6);">
    <div class="d-flex justify-content-center align-items-center h-100">
      <h1 class="text-white mb-0">Page title</h1>
    </div>
  </div>
</div>
'''


cta_langing_page = html.Div([
                  dbc.Row([
                      # LOGO + SLOGAN
                  ]),
                  dbc.Row(dbc.Button("Forecast", outline=True, color="warning", className="rounded-pill", style={"height": "10vh","width": "20vw"})),
                    ], className="d-flex justify-content-center align-items-center")

panel_video = html.Section([
        html.Video([
                          html.Source(src="/assets/videos/background_video.mp4"),
                      ],
              autoPlay=True,
              loop=True,
              style={
                      "height": "100%",
                      "width": "100%",
                      "object-fit": "cover",
                      "position":"relative",
                      "top":0,
                      "left":0,
                      "display":"block",
                      "zIndex":0
                      # "z-index":1,
                      # "top":"0%"
            }),

        dbc.Row([
                cta_langing_page
                # html.Div([
                #     cta_langing_page
                # ], 
                # className="d-flex justify-content-center align-items-center",
                # )
            ],align="center", style={
                    "position": "absolute",
                    "background": "rgba(0, 0, 0, 0.85)",
                    # "height": "100%",
                    "width": "100%",
                    "height" :"100vh",
                    # "padding": "20px",
                    "top":"0%",
                    "zIndex":1
                    }
            )
  ], style={
          "display":"flex",
          "justify-content" :"center",
          "align-items": "center",
          "width": "100%",
          "height" :"100vh",
          # "overflow" :"visible"
  })




            

# panel = html.Div([                                 # IMAGE BACKGROUND
#             html.Div([
#                     html.Div([
#                         html.H1("Page title",className="text-white mb-0"),
#                     ], 
#                     className="d-flex justify-content-center align-items-center h-100",
#                     )
#                 ], 
#                 className="mask",
#                 style={"background-color": "rgba(0, 0, 0, 0.6)","height": "100vh"})
#         ], className="bg-image",
#         style={"background-image": "url('https://mdbcdn.b-cdn.net/img/new/fluid/nature/012.webp')",
#             "height": "100vh"}
#         )

presentation = html.Div([
      html.Div([
          html.Div([
                  dbc.Card([
                  dbc.CardBody([
                      html.I(className="fas fa-brain fa-2x mb-3"),
                      html.H4("7:45PM"),
                      html.P("May 21",className="small text-white-50 mb-4"),
                      html.P("Lorem ipsum dolor sit amet, quo ei simul congue exerci, ad nec admodum perfecto mnesarchum, vim ea mazim fierent detracto. Ea quis iuvaret expetendis his, te elit voluptua dignissim per, habeo iusto primis ea eam."),
                      html.H6("New", className="badge bg-body-tertiary text-black mb-0"),
                      html.H6("Admin", className="badge bg-body-tertiary text-black mb-0"),
                  ],className="p-4")
              ],className="gradient-custom")
          ], className="timeline-4 left-4"),


          html.Div([
                  dbc.Card([
                  dbc.CardBody([
                      html.I(className="fas fa-camera fa-2x mb-3"),
                      html.H4("7:45PM"),
                      html.P("May 21",className="small text-white-50 mb-4"),
                      html.P("Lorem ipsum dolor sit amet, quo ei simul congue exerci, ad nec admodum perfecto mnesarchum, vim ea mazim fierent detracto. Ea quis iuvaret expetendis his, te elit voluptua dignissim per, habeo iusto primis ea eam."),
                      html.H6("New", className="badge bg-body-tertiary text-black mb-0"),
                      html.H6("Admin", className="badge bg-body-tertiary text-black mb-0"),
                  ],className="p-4")
              ],className="gradient-custom-4")
          ], className="timeline-4 right-4"),


          html.Div([
                  dbc.Card([
                  dbc.CardBody([
                      html.I(className="fas fa-brain fa-2x mb-3"),
                      html.H4("7:45PM"),
                      html.P("May 21",className="small text-white-50 mb-4"),
                      html.P("Lorem ipsum dolor sit amet, quo ei simul congue exerci, ad nec admodum perfecto mnesarchum, vim ea mazim fierent detracto. Ea quis iuvaret expetendis his, te elit voluptua dignissim per, habeo iusto primis ea eam."),
                      html.H6("New", className="badge bg-body-tertiary text-black mb-0"),
                      html.H6("Admin", className="badge bg-body-tertiary text-black mb-0"),
                  ],className="p-4")
              ],className="gradient-custom")
          ], className="timeline-4 left-4"),
      
    ], className="main-timeline-4 text-white")
],className="container")


layout = html.Div([
    html.Div([panel_video], className="mb-3"),
    html.Div([presentation], className="mb-3")
])