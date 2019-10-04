import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly
import plotly.graph_objects as go
import plotly.express as px
import os



def head_title(word):
    return html.Div([
        html.H1(word, style={"textAlign":"center"})
    ], style={"backgroundColor": "#fbffb9"})


app = dash.Dash(__name__)

server = app.server

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
                        html.Div([dcc.Link("为什么我来这里", href="/reasons")]),
                        html.Div([dcc.Link("数据可视化", href="/datavisualization")]),
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
            [dcc.Location(id="url", refresh=False), html.Div(id="contents")],
            style={
                "width": "80%",
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
], style={"height": 800})

self_intro = html.Div([
    head_title("你好，自我介绍"),
    html.Div([
        html.Div([
        html.Img(src="assets/me.jpg", style={"width": "60%", "margin": "20%"})
        ]),
    ], style={"width": "40%", "float": "left"}),
    html.Div([
        html.Div([
        html.P("我叫 小川 英幸（wechat： hide_xiao）"),
        html.P("我来自,日本京都（你知吗？）"),
        html.P("我的事业"),
        html.P("· I worked as a trader and analyst at Financial Institute."),
        html.P("· I started using Python 5 years ago(numpy pandas matoplotlib)."),
        html.P("· I founded a company named Chomoku(长目)."),
        html.Div([
        html.Img(src="assets/hannnari.png", style={"width":"50%"})], style={"textAlign": "center"}),
        ], style={"fontSize": 25,"margin": "5%"}),
    ], style={"width": "60%", "display":"inline-block"})
])

reasons = html.Div([
        head_title("为什么我来 PyCon CHINA 北京？"),
        html.Div([
            # あとから手直しする
            dcc.Markdown("""
                * 1.I study Chinese for a year and half.    
                    * I wanted to learn for a long time.Because I have been interested in Chinese Culture!      
                    * My company name "Chomoku" is from old chinese word ["长目飞耳"](https://baike.baidu.com/item/%E9%95%BF%E7%9B%AE%E9%A3%9E%E8%80%B3).
                * 2.Many People says "Chinese Programmer quiality is the best in the world."
                    * My friend who work at chinese company said so.
                    * I want to meet.
                * 3.I read a book titled "Ant Financial".
                    * It has many impressive scenes.
                    * The most impressive scene was the they visited Square's office and disappointment of the expensive fee of the servise.
                * 4.I found PyCon China Beijing.
                    * I accidentally found this event in August.
                    * Then I was preparing for PyConJP talk.I entryed with same theme.
            """)
        ], style={"margin": "5%", "fontSize": 25})
])

datavisualization = html.Div([

])


@app.callback(Output("contents", "children"), [Input("url", "pathname")])
def update_pages(pathname):
    if pathname == "/self-introduce":
        return self_intro
    elif pathname == "/reasons":
        return reasons
    elif pathname == "/datavisualization":
        return datavisualization
    else:
        return title


if __name__ == "__main__":
    app.run_server(debug=True)
