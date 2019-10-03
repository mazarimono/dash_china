import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly
import plotly.graph_objects as go
import plotly.express as px



app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.P("用Dash的可视化", style={"fontSize": 30}),
                html.P("Today's Menu", style={"fontSize": 20}),
                html.Div(
                    [
                        html.Div([dcc.Link("TiTle", href="/")]),
                        html.Div([dcc.Link("自我介绍", href="/self-introduce")]),
                        html.Div([dcc.Link("为什么我来这里", href="/why-iam-here")]),
                        html.Div([html.Img(src="assets/logo-simple.png",
                        style={"width": "70%"})])
                    ]
                ),
            ],
            id="title",
            style={
                "width": "20%",
                "height": 800,
                "backgroundColor": "#C5E99B",
                "textAlign": "center",
                "float": "left",
                "borderRadius": "10px",
            },
        ),
        html.Div(
            [dcc.Location(id="url")],
            id="contents",
            style={
                "width": "80%",
                "height": 800,
                "backgroundColor": "#D7FFF1",
                "display": "inline-block",
                "borderRadius": "10px",
            },
        ),
    ],
    style={"width": "95%", "margin": "auto"},
)

title = html.Div([
    html.Img(src="assets/chomoku-logo.png",
    style={"width": "20%", "marginLeft": "75%", "marginTop": "5%"}),
    html.P("用 Dash 实现交互式数据可视化", style={"textAlign": "center", "marginTop": "10%", "fontSize": 60}),
    html.P("PyCon China 北京 2019/10/19",
    style={"marginTop": "10%", "textAlign": "right", "marginRight": "5%", "fontSize": 30}),
    html.P("长目 CEO 小川 英幸", style={"textAlign": "right", "marginRight": "5%", "fontSize": 30})
])

self_intro = html.Div([
    html.Div([
    html.H1("你好，自我介绍", style={"textAlign": "center"})], style={"backgroundColor": "#fbffb9"}),
    html.Div([
        html.Div([
        html.Img(src="assets/me.jpg", style={"width": "60%", "margin": "20%"})
        ]),
    ], style={"width": "40%", "float": "left"}),
    html.Div([
        html.Div([
        html.P("我叫 小川 英幸（wechat： hide_xiao）"),
        html.P("我来自 日本 京都（你知吗？）"),

        ], style={"fontSize": 30, "textAlign": "center", "margin": "5%"}),
    ], style={"width": "60%", "display":"inline-block"})
])

reasons = html.Div([html.H1("Why I am here.")])


@app.callback(Output("contents", "children"), [Input("url", "pathname")])
def update_pages(pathname):
    if pathname == "/self-introduce":
        return self_intro
    elif pathname == "/why-iam-here":
        return reasons
    else:
        return title


if __name__ == "__main__":
    app.run_server(debug=True)
