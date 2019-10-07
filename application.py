import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import dash_canvas
from dash.dependencies import Input, State, Output
from dash.exceptions import PreventUpdate

import plotly
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import skimage
import json
import os

from dash_canvas.components import image_upload_zone
from dash_canvas.utils import (
    parse_jsonstring,
    superpixel_color_segmentation,
    image_with_contour,
    image_string_to_PILImage,
    array_to_data_url,
)
from dash_canvas.components import image_upload_zone


# data read
citydata = pd.read_csv("assets/citydata.csv", index_col=0)

# image read
filepath = "assets/me.jpg"
filename = array_to_data_url(skimage.io.imread(filepath))

# mapbox
px.set_mapbox_access_token(
    "pk.eyJ1IjoibWF6YXJpbW9ubyIsImEiOiJjanA5Y3I\
xaWsxeGtmM3dweDh5bjgydGFxIn0.3vrfsqZ_kGPGhi4_npruGg"
)

# markdownのスタイル

mkstyle_ins = {
    "fontSize": 30,
    "width": "80%",
    "margin": "auto",
    "backgroundColor": "white",
    "padding": "3%",
    "borderRadius": 10,
}

mkstyle_ous = {
    "width": "80%",
    "margin": "auto",
    "backgroundColor": "#cbe86e",
    "padding": "3%",
    "margin": "3% auto ",
    "borderRadius": 15,
}

# タイトル用の関数
def head_title(word):
    return html.Div(
        [html.H1(word, style={"textAlign": "center"})],
        style={"backgroundColor": "#fbffb9"},
    )


app_dash = dash.Dash(__name__)

app_dash.config.suppress_callback_exceptions = True


# layout
# -------------------------------------------------------------------------------------

app_dash.layout = html.Div(
    [
        html.Div(
            [
                html.P("用Dash的可视化", style={"fontSize": 30}),
                html.Div(
                    [
                        html.Div([dcc.Link("TiTle", href="/")]),
                        html.Div([dcc.Link("自我介绍", href="/self-introduce")]),
                        html.Div([dcc.Link("为什么我来这里", href="/reasons")]),
                        html.Div([dcc.Link("Today's Menu", href="/menu")]),
                        html.Div([dcc.Link("数据可视化", href="/datavisualization")]),
                        html.Div([dcc.Link("数据可视化2", href="/datavisualization_human")]),
                        html.Div(
                            [dcc.Link("数据可视化3", href="/interactive_visualization")]
                        ),
                        html.Div([dcc.Link("数据可视化4", href="/visualization_tools")]),
                        html.Div([dcc.Link("about_dash", href="/about_dash")]),
                        html.Div([dcc.Link("dash_basic", href="/dash_basic")]),
                        html.Div([dcc.Link("dash_graphs", href="/dash_graphs")]),
                        html.Div(
                            [dcc.Link("dash_components", href="/dash_components")]
                        ),
                        html.Div(
                            [
                                html.Img(
                                    src="assets/logo-simple.png", style={"width": "70%"}
                                )
                            ]
                        ),
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

title = html.Div(
    [
        html.Img(
            src="assets/chomoku-logo.png",
            style={"width": "20%", "marginLeft": "75%", "marginTop": "5%"},
        ),
        html.P(
            "用 Dash 实现交互式数据可视化",
            style={"textAlign": "center", "marginTop": "10%", "fontSize": 60},
        ),
        html.P(
            "PyCon China 北京 2019/10/19",
            style={
                "marginTop": "10%",
                "textAlign": "right",
                "marginRight": "5%",
                "fontSize": 30,
            },
        ),
        html.P(
            "长目 CEO 小川 英幸",
            style={"textAlign": "right", "marginRight": "5%", "fontSize": 30},
        ),
    ],
    style={"height": 800},
)

self_intro = html.Div(
    [
        head_title("你好，自我介绍"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="assets/me.jpg", style={"width": "60%", "margin": "20%"}
                        ),
                        html.Img(
                            src="assets/hannnari.png",
                            style={"width": "60%", "marginLeft": "20%"},
                        ),
                    ]
                )
            ],
            style={"width": "40%", "float": "left"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("我叫 小川 英幸（wechat： hide_xiao）"),
                        html.P("我来自,日本京都（你知吗？）"),
                        dcc.Graph(
                            figure=px.scatter_mapbox(
                                citydata,
                                lat="lat",
                                lon="long",
                                text="city",
                                size="pop",
                                color="pop",
                                zoom=3,
                                color_continuous_scale=px.colors.sequential.Rainbow,
                            )
                        ),
                        html.Br(),
                        html.P("我的事业"),
                        html.P(
                            "· I worked as a trader and analyst at Financial Institute."
                        ),
                        html.P(
                            "· I started using Python 5 years ago(numpy pandas matoplotlib)."
                        ),
                        html.P("· I founded a company named Chomoku(长目)."),
                    ],
                    style={"fontSize": 25, "margin": "5%"},
                )
            ],
            style={"width": "60%", "display": "inline-block"},
        ),
    ]
)

reasons = html.Div(
    [
        head_title("为什么我来 PyCon CHINA 北京？"),
        html.Div(
            [
                # あとから手直しする
                dcc.Markdown(
                    """
                1. I study Chinese for a year and half.    
                    - I wanted to learn for a long time.Because I have been interested in Chinese Culture!      
                    - My company name "Chomoku" is from old chinese word ["长目飞耳"](https://baike.baidu.com/item/%E9%95%BF%E7%9B%AE%E9%A3%9E%E8%80%B3).
                1. Many People says "Chinese Programmer quiality is the best in the world."
                    - My friend who work at chinese company said so.
                    - I want to meet.
                1. I read a book titled "Ant Financial".
                    - It has many impressive scenes.
                    - The most impressive scene was the they visited Square's office and disappointment of the expensive fee of the servise.
                1. I found PyCon China Beijing.
                    - I accidentally found this event in August.
                    - Then I was preparing for PyConJP talk.I entryed with same theme.
            """
                )
            ],
            style={"margin": "5%", "fontSize": 25},
        ),
    ]
)

# Today's Munu

menu = html.Div(
    [
        head_title("Today's Menu"),
        html.Div(
            [
                dcc.Markdown(
                    """
        1. About Data Visualization.
            - before talking about dash, talking about data visualization.
        1. About Dash.      
        1. Use cases and about data analysis.      

    """
                )
            ],
            style={"margin": "5%", "fontSize": 25},
        ),
    ]
)


# Dashについて話す前に、そもそものデータビジュアライゼーションについて話します。
# ここは頑張らずにサンプルデータを利用する。 iris, gapminder,
datavisualization = html.Div(
    [
        head_title("关于数据可视化"),
        # About Data visualization.
        # add some samples to understand what is data visualization.
        # ここでデータ分析において探索的な分析、特徴量の探索が必要であることに触れる。
        # この次に人間にとってわかりやすいという話を行う。
        html.Div(
            [html.Div(id="whywedata-v-child", style={"margin": "5%", "fontSize": 25})],
            id="whywedata-v",
            n_clicks=0,
        ),
    ]
)

## 1 のところがずれるし直したい。
@app_dash.callback(
    Output("whywedata-v-child", "children"), [Input("whywedata-v", "n_clicks")]
)
def update_markdown(n_clicks):
    if n_clicks % 2 == 0:
        return dcc.Markdown(
            """
            1. Why we do data visualization?     
                - When we analyze data, there are 5steps.     
                    - 1.Define your questions & goals.     
                    - 2.Collect data.      
                    - 3.Data Preprocessing.      
                    - 4.Exploratory data analysis & Feature Engineering.      
                    - 5.Evaluate Model and Algorithms.      
            """
        )
    else:
        return dcc.Markdown(
            """
            1. Why we do data visualization?     
                - When we analyze data, there are 5steps.     
                    - 1.Define your questions & goals.     
                    - 2.Collect data.      
                    - 3.Data Preprocessing.      
                    ## 4.Exploratory data analysis.      
                    - 5.Evaluate Model and Algorithms.    

                ### Exploratory data analysis     
                - Analyze data sets and summarize their main charactors.
                - To know buissiness.
                - Feature Enginnering.     
                ### And This step often with visual methods.
            """
        )


iris = plotly.data.iris()

datavisualization_human = html.Div(
    [
        head_title("关于数据可视化2"),
        # ここで可視化した方が人間にとってわかりやすいという話を行う。
        html.Div(
            [
                html.H2(
                    "Easier to Understand(for humans).", style={"textAlign": "center"}
                ),
                html.Button("change button", id="table_to_chart", n_clicks=0),
                html.Div(id="showdata_for_humans"),
            ],
            style={"margin": "5%"},
        ),
    ]
)


@app_dash.callback(
    Output("showdata_for_humans", "children"), [Input("table_to_chart", "n_clicks")]
)
def change_table_to_chart(n_clicks):
    if n_clicks % 2 == 0:
        return dash_table.DataTable(
            columns=[{"id": i, "name": i} for i in iris.columns],
            data=iris.to_dict("records"),
            style_cell={"textAlign": "center"},
        )
    else:
        return dcc.Graph(
            figure=px.scatter_matrix(
                iris,
                dimensions=[
                    "sepal_width",
                    "sepal_length",
                    "petal_width",
                    "petal_length",
                ],
                color="species",
            )
        )


gapminder = plotly.data.gapminder()
gapminder5 = gapminder[
    gapminder["country"].isin(
        ["Canada", "Switzerland", "Denmark", "United States", "Australia"]
    )
]


interactive_visualization = html.Div(
    [
        head_title("关于数据可视化3"),
        html.Div(
            [
                html.H2(
                    "Normal Visualization(with using gapminder data)",
                    style={"textAlign": "center"},
                ),
                html.Button("change button", id="normal_button", n_clicks=0),
                html.Div(id="normal_visualization"),
                html.Div(
                    [
                        html.H2(
                            "Interactive Visualization", style={"textAlign": "center"}
                        ),
                        html.Button(
                            "change button", id="interactive_button", n_clicks=0
                        ),
                        html.Div(id="interactive_viz"),
                        dcc.Checklist(
                            id="interactive_checklist",
                            options=[
                                {"label": i, "value": i}
                                for i in gapminder.country.unique()
                            ],
                            labelStyle={"display": "inline-block"},
                            value=[
                                "Canada",
                                "Switzerland",
                                "Denmark",
                                "United States",
                                "Australia",
                            ],
                        ),
                    ]
                ),
            ],
            style={"margin": "5%"},
        ),
    ]
)


@app_dash.callback(
    Output("normal_visualization", "children"), [Input("normal_button", "n_clicks")]
)
def update_to_normal(n_clicks):
    if n_clicks % 2 == 0:
        return dcc.Graph(
            figure=px.line(
                gapminder5,
                x="year",
                y="gdpPercap",
                color="country",
                title="Normal Visualization",
            )
        )
    elif n_clicks % 2 == 1:
        return dcc.Graph(
            figure=px.line(
                gapminder,
                x="year",
                y="gdpPercap",
                color="country",
                title="Normal Visualization(with more data)",
            )
        )


# よりによって、香港と中国が一緒になって、中国が動かない。。。困った。全部の国が選べるボタンも欲しい。


@app_dash.callback(
    Output("interactive_viz", "children"),
    [Input("interactive_button", "n_clicks"), Input("interactive_checklist", "value")],
)
def update_interactive(n_clicks, country_list):
    gapp = gapminder[gapminder["country"].isin(country_list)]
    if n_clicks % 2 == 0:
        return dcc.Graph(
            figure=px.line(
                gapp,
                x="year",
                y="gdpPercap",
                color="country",
                title="Interactive Visualization",
            )
        )
    else:
        return dcc.Graph(
            figure=px.scatter(
                gapp,
                x="gdpPercap",
                y="lifeExp",
                size="pop",
                color="continent",
                hover_name="country",
                animation_frame="year",
                size_max=45,
                range_x=[100, 100000],
                range_y=[30, 90],
                log_x=True,
            )
        )


visualization_tools = html.Div(
    [
        head_title("关于数据可视化4"),
        html.Div(
            [
                html.H2("Visualization Tools", style={"textAlign": "center"}),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            ## There are many visualization tools
            ### BI Tools:(1)
            #### Tableau, Microsoft Power BI, Qlik, SAP BI, Google Data Studio
            ### Libraries
            #### D3, Highcharts, Matplotlib, Bokeh, etc....
            ### Interactive Web Framework
            #### Shiny(R), Dash(Python), Panel(Python)
        """
                        ),
                        html.Div(
                            [
                                html.A(
                                    "(1) from garter report",
                                    href="https://www.gartner.com/reviews/market/analytics-business-intelligence-platforms",
                                )
                            ],
                            style={"textAlign": "right"},
                        ),
                    ]
                ),
            ],
            style={"margin": "5%"},
        ),
    ]
)

about_dash = html.Div(
    [
        head_title("About Dash"),
        html.Div(
            [
                dcc.Markdown(
                    """
            - Dash is Analytical web application.
                - Open Souce Python library.
                - made by [plotly](https://plot.ly/).
                - Write code with only Python.
                - Made by Flask、plotly.js、react.js.
                - [Document](https://dash.plot.ly/)
            - Interactive data visualization, and easy to share.
                - Data Visualozation with Plotly.
                - A lot of data can watch.
                - Easy to share on the web.
            - There are many other components besides graphs.
                - Dash_table、Dash_Canvas、Dash-Bio and so on.
                - You can make a component!
        """
                )
            ],
            style={"margin": "5%", "fontSize": 30},
        ),
    ]
)

dash_basic = html.Div(
    [
        head_title("how to make dash application."),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="hello-graph",
                            figure={
                                "data": [
                                    {
                                        "x": [1, 2, 3],
                                        "y": [2, 3, 4],
                                        "type": "bar",
                                        "name": "Kyoto",
                                    },
                                    {
                                        "x": [1, 2, 3],
                                        "y": [4, 2, 4],
                                        "type": "bar",
                                        "name": "Tokyo",
                                    },
                                    {
                                        "x": [1, 2, 3],
                                        "y": [3, 1, 4],
                                        "type": "bar",
                                        "name": "Osaka",
                                    },
                                ],
                                "layout": {"title": "Dash DataViz", "height": 400},
                            },
                        ),
                        html.Div(id="hello-graph-callback", style={"fontSize": 30}),
                    ],
                    style={"width": "70%", "margin": "auto"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Dash application made by layout and callbacks.",
                                    style={"textAlign": "center"},
                                )
                            ],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                            - Layout
                                - make what looks like
                                - use components
                            - callbacks
                                - Keys to make applications interactive.
                                - Use Input State Output
                        """,
                                    style=mkstyle_ins,
                                )
                            ],
                            style=mkstyle_ous,
                        ),
                    ]
                ),
                # コードのマークダウンを直す。
                html.Div(
                    [
                        html.P("Code ", style={"fontSize": 30}),
                        dcc.Markdown(
                            """
            import dash     
            import dash_core_components as dcc     
            import dash_html_components as html     
                 
            app = dash.Dash()      
                     
           \# Create a layout     
                  
            app.layout = html.Div(     
                    children=[    
                    dcc.Graph(    
                        id="hello-graph",    
                        figure={    
                            "data": [    
                                {"x": [1, 2, 3], "y": [2, 3, 4],    
                                  "type": "bar", "name": "Kyoto"},    
                                {"x": [1, 2, 3], "y": [4, 2, 4],    
                                  "type": "bar", "name": "Tokyo"},    
                                {"x": [1, 2, 3], "y": [3, 1, 4],    
                                  "type": "bar", "name": "Osaka"},    
                                ],    
                            "layout": {"title": "Dash DataViz", "height": 800},    
                        },    
                    ),    
                    html.Div(id="hello-graph-callback", style={"fontSize":30}),    
                ]    
            )     
                  
            \# Create a callback    
            @app.callback(Output("hello-graph-callback", "children"),         
                        \[Input("hello-graph", "hoverData")\]\)             
            def hello_graph_callback(hoverData):         
                return json.dumps(hoverData)         

            app.run_server(debug=True)     
            """,
                            style=mkstyle_ins,
                        ),
                    ],
                    style=mkstyle_ous,
                ),
            ]
        ),
    ]
)


@app_dash.callback(
    Output("hello-graph-callback", "children"), [Input("hello-graph", "hoverData")]
)
def hello_graph_callback(hoverData):
    return json.dumps(hoverData)


# dash_graphs
### Think about graphs to show sample.
graphModuleList = ["dash", "plotly.graph_objects", "plotly_express"]
go_graphTypes = []
px_graphTypes = []

dash_graphs = html.Div(
    [
        head_title("Graphs"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            """
                Dash graphs need to use dash_core_components module's Graph class.
                Inside of it, you can use plotly! Off cource you can write it by dash.
                        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Graph by Modules", style={"textAlign": "center"}
                                )
                            ],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        dcc.RadioItems(
                            id="graphs_radio",
                            options=[{"label": i, "value": i} for i in graphModuleList],
                            value="dash",
                            labelStyle={"display": "inline-block", "margin": "1%"},
                        ),
                    ],
                    style={"fontSize": 30},
                ),
                html.Div(id="graph_by_module"),
                html.Div(
                    [html.H2("Graph Types", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                    [Plotly.py](https://plot.ly/python/) library supports over 40 chart types.
                    Here shows some exmples.
                    """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                dcc.RadioItems(
                    id="graphModule",
                    options=[
                        {"label": i, "value": i}
                        for i in ["plotly.graph_objects", "plotly.express"]
                    ],
                    value="plotly.graph_objects",
                    labelStyle={
                        "display": "inline-block",
                        "margin": "2%",
                        "fontSize": 30,
                    },
                ),
                html.Div(id="graphType"),
            ],
            style={"margin": "5%"},
        ),
    ]
)

# マークダウン内のコメントアウトの処理

# グラフモジュールによる違いを見せるコールバック
@app_dash.callback(
    Output("graph_by_module", "children"), [Input("graphs_radio", "value")]
)
def update_by_graph_module(module_name):
    gapminder2007 = gapminder[gapminder["year"] == 2007]
    if module_name == "dash":
        return html.Div(
            [
                dcc.Graph(
                    figure={
                        "data": [
                            {
                                "x": gapminder2007["gdpPercap"],
                                "y": gapminder2007["lifeExp"],
                                "mode": "markers",
                            }
                        ],
                        "layout": {
                            "height": 400,
                            "xaxis": {"title": "gdpPercap(log)", "type": "log"},
                            "yaxis": {"title": "lifeExp"},
                            "title": "Graph by Dash",
                        },
                    }
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            dcc.Graph(figure={"data": [{"x": gapminder2007["gdpPercap"], "y":gapminder2007["lifeExp"],"mode":"markers"
            }], "layout": {"height": 400, "xaxis": {"title": "gdpPercap(log)", "type": "log"}, "yaxis":{"title": "lifeExp"}, "title":"Graph by Dash"}})
            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
            ]
        )

    elif module_name == "plotly.graph_objects":
        return html.Div(
            [
                dcc.Graph(
                    figure={
                        "data": [
                            go.Scatter(
                                x=gapminder2007["gdpPercap"],
                                y=gapminder2007["lifeExp"],
                                mode="markers",
                            )
                        ],
                        "layout": go.Layout(
                            height=400,
                            xaxis={"title": "gdpPercap(log)", "type": "log"},
                            yaxis={"title": "lifeExp"},
                            title="Graph by plotly.graph_objects",
                        ),
                    }
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            dcc.Graph(figure={"data": [go.Scatter(x=gapminder2007["gdpPercap"], y=gapminder2007["lifeExp"], mode="markers")],
            "layout":go.Layout(height=400, xaxis={"title": "gdpPercap(log)", "type":"log"}, yaxis={"title":"lifeExp"}, title= "Graph by plotly.graph_objects")})
            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
            ]
        )

    else:
        return html.Div(
            [
                dcc.Graph(
                    figure=px.scatter(
                        gapminder2007,
                        x="gdpPercap",
                        y="lifeExp",
                        height=400,
                        log_x=True,
                        title="Graph by plotly.express",
                    )
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            dcc.Graph(figure=px.scatter(gapminder2007, x="gdpPercap", y="lifeExp", height=400, log_x=True, title="Graph by plotly.express"))
            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
            ]
        )


# グラフサンプルを表示するコールバック
# 時間があれば作りこみたい。今はとりあえずいくつか作りたい。

# Components
params = ["Weight", "Torque", "Width", "Height"]

dash_components = html.Div(
    [
        head_title("Components"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash's layout must be made by components.I will show 7 components ready to use.
            [You can make your own components](https://dash.plot.ly/plugins)!
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [html.H2("dash_html_components", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash_html_components provide HTML Tags as Python Classes.     
                 
            if you want to write       
                  
            ```
            <h1>Hello China!</h1>
            ```
                   
            with Dash_html_components module      
                   
            ```
            import dash_html_components as html
            html.H1("Hello China!")
            ```

            Dash_components_components has 131 classes. Covers all HTML tags? I have no idea.

        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [html.H2("Dash_Core_Components", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash_Core_Components provides components like sliders, dropdowns, graphs and more.
            Many conponents fires callback. And application gets interactive.
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("X axis value: ", style={"fontSize": 25}),
                                dcc.Dropdown(
                                    id="dcc_dd_x",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in gapminder.columns[3:6]
                                    ],
                                    value="lifeExp",
                                ),
                            ],
                            style={"width": "49%", "float": "left"},
                        ),
                        html.Div(
                            [
                                html.P("Y axis value: ", style={"fontSize": 25}),
                                dcc.Dropdown(
                                    id="dcc_dd_y",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in gapminder.columns[3:6]
                                    ],
                                    value="pop",
                                ),
                            ],
                            style={"width": "49%", "display": "inline-block"},
                        ),
                        html.Div(id="show_dccs_graph"),
                        # The reason is not clear but cannot be displayed...(RangeSlider)
                        # Try to add RangeSlider Later///
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H2("Dash Table", style={"textAlign": "center"})],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                Dash Datatable is interactive table. This can be use like Excel.
            """,
                                    style=mkstyle_ins,
                                )
                            ],
                            style=mkstyle_ous,
                        ),
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="table-editing-simple",
                                    columns=(
                                        [{"id": "Model", "name": "Model"}]
                                        + [{"id": p, "name": p} for p in params]
                                    ),
                                    data=[
                                        dict(Model=i, **{param: 0 for param in params})
                                        for i in range(1, 5)
                                    ],
                                    editable=True,
                                ),
                                dcc.Graph(id="table-editing-simple-output"),
                            ]
                        ),
                    ]
                ),
                # dash_daq
                html.Div(
                    [html.H2("Dash Daq", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash Daq is for Data aquisition. It can make beautiful UIs.Tools for Measuring 
            such as voltage,temperature, pressure and more. 
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        dcc.Interval(
                            id="daq-interval",
                            interval=1000,
                            n_intervals=0,
                            disabled=True,
                        ),
                        daq.PowerButton(
                            id="daq-powerbutton", on=False, size=100, color="green"
                        ),
                        html.Div(id="daq-realtime"),
                    ]
                ),
                # dash_canvas
                html.Div(
                    [html.H2("Dash Canvas", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash Canvas is drawing and annotation for image processing. Annotation for 
            Machine Learning training set and more.
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dash_canvas.DashCanvas(
                                    id="canvas-bg",
                                    width=500,
                                    filename=filename,
                                    lineWidth=8,
                                    goButtonTitle="Remove background",
                                    hide_buttons=["line", "zoom", "pan"],
                                )
                            ],
                            style={"display": "inline-block", "marginRight": "5%"},
                        ),
                        html.Div(
                            [html.Img(id="seg-image", width=500)],
                            style={"display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Link(
                                    "Dash Canvas Document",
                                    href="https://dash.plot.ly/canvas",
                                )
                            ],
                            style={"margin": "5%", "textAlign": "center"},
                        ),
                    ]
                ),
                html.Div(
                    [html.H2("Dash Cytoscape", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                        Dash Cytoscape is a network visualization components. Using Cytoscape.js.
                        
                    """
                        )
                    ]
                ),
            ],
            style={"margin": "5%"},
        ),
    ]
)

# dcc sample callback
@app_dash.callback(
    Output("show_dccs_graph", "children"),
    [Input("dcc_dd_x", "value"), Input("dcc_dd_y", "value")],
)
def update_xy_data_graph(x_value, y_value):
    return dcc.Graph(
        figure=px.scatter(
            gapminder,
            x=x_value,
            y=y_value,
            color="year",
            hover_name="country",
            log_x=True,
            log_y=True,
            title="Gapminder Chart X: {}, Y: {}".format(x_value, y_value),
        )
    )


# dash_table sample callback


@app_dash.callback(
    Output("table-editing-simple-output", "figure"),
    [Input("table-editing-simple", "data"), Input("table-editing-simple", "columns")],
)
def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    return {
        "data": [
            {
                "type": "parcoords",
                "dimensions": [
                    {"label": col["name"], "values": df[col["id"]]} for col in columns
                ],
            }
        ]
    }


# dash_daq sample callback
@app_dash.callback(Output("daq-interval", "disabled"), [Input("daq-powerbutton", "on")])
def wakeupCall(switch):
    if switch == 1:
        return False
    else:
        return True


@app_dash.callback(
    Output("daq-realtime", "children"), [Input("daq-interval", "n_intervals")]
)
def wakeupDaq(n_intervals):
    if n_intervals:
        n1 = np.random.random() * 10
        n2 = np.random.random() * 10
        n3 = np.random.random() * 10
        n4 = np.random.random() * 10
        n5 = np.random.random() * 10
        n6 = np.random.random() * 10
        n7 = np.random.random() * 10
        n_sum = n1 + n2 + n3 + n4 + n5 + n6 + n7

        return html.Div(
            [
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n1,
                    size=400,
                    style={"display": "inline-block"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n2,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n3,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n4,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n5,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n6,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n7,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.LEDDisplay(value=n_sum),
            ],
            style={"textAlign": "center", "margin": "5%"},
        )


# dash canvas


@app_dash.callback(
    Output("seg-image", "src"),
    [Input("canvas-bg", "json_data"), Input("canvas-bg", "image_content")],
)
def update_figure(string, image):
    if string:
        if image is None:
            im = skimage.io.imread(filepath)
        else:
            im = image_string_to_PILImage(image)
            im = np.asarray(im)
        shape = im.shape[:2]
        try:
            mask = parse_jsonstring(string, shape=shape)
        except IndexError:
            raise PreventUpdate
        if mask.sum() > 0:
            seg = superpixel_color_segmentation(im, mask)
        else:
            seg = np.ones(shape)
        fill_value = 255 * np.ones(3, dtype=np.uint8)
        dat = np.copy(im)
        dat[np.logical_not(seg)] = fill_value
        return array_to_data_url(dat)
    else:
        raise PreventUpdate


# Page Lotation Callback
# ------------------------------------------------------------------------


@app_dash.callback(Output("contents", "children"), [Input("url", "pathname")])
def update_pages(pathname):
    if pathname == "/self-introduce":
        return self_intro
    elif pathname == "/reasons":
        return reasons
    elif pathname == "/menu":
        return menu
    elif pathname == "/datavisualization":
        return datavisualization
    elif pathname == "/datavisualization_human":
        return datavisualization_human
    elif pathname == "/interactive_visualization":
        return interactive_visualization
    elif pathname == "/visualization_tools":
        return visualization_tools
    elif pathname == "/about_dash":
        return about_dash
    elif pathname == "/dash_basic":
        return dash_basic
    elif pathname == "/dash_graphs":
        return dash_graphs
    elif pathname == "/dash_components":
        return dash_components
    else:
        return title


if __name__ == "__main__":
    app_dash.run_server(debug=True)
