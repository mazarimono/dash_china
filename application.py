import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import os

# data read
citydata = pd.read_csv("assets/citydata.csv", index_col=0)


# mapbox
px.set_mapbox_access_token(
    "pk.eyJ1IjoibWF6YXJpbW9ubyIsImEiOiJjanA5Y3I\
xaWsxeGtmM3dweDh5bjgydGFxIn0.3vrfsqZ_kGPGhi4_npruGg"
)

#
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
                html.Div([
                    html.Div([
                        html.H2("Dash application made by layout and callbacks.", style={"textAlign":"center"})
                    ], style={"backgroundColor": "#fbffb9"}),
                    html.Div([
                        dcc.Markdown("""
                            - Layout
                                - make what looks like
                                - use components
                            - callbacks
                                - Keys to make applications interactive.
                                - Use Input State Output
                        """),

                    ], style={"fontSize": 30, "width": "80%", "margin": "5% auto 5%", "backgroundColor": "#fbffb9", "padding":"2%", "borderRadius": 10})
                ]),
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
            style={
                "fontSize": 30,
                "width": "80%",
                "margin": "auto",
                "backgroundColor": "white",
                "padding": "3%",
                "borderRadius": 10,
                },
            ), ], style={
                "width": "80%",
                "margin": "auto",
                "backgroundColor": "#cbe86e",
                "padding": "3%",
                "borderRadius": 15,
                    },
                ),
            ]
        ),
    ]
)

dash_graphs = html.Div([
    head_title("Graphs"),
    html.Div([
        
    ])
])

@app_dash.callback(Output("hello-graph-callback", "children"),
            [Input("hello-graph", "hoverData")])
def hello_graph_callback(hoverData):
    return json.dumps(hoverData)

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
    else:
        return title


if __name__ == "__main__":
    app_dash.run_server(debug=True)
