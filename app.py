# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
local_stylesheets = ["./assets/styles.css"]
app = dash.Dash(__name__, external_stylesheets=local_stylesheets)

app.layout = html.Div(
    children=[
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Tab one",
                    children=[
                        dcc.Markdown("""hello i'm tab one"""),
                        dcc.Markdown("""![city](./assets/images/tab1.jpg)"""),
                    ],
                ),
                dcc.Tab(
                    label="Tab two",
                    children=[
                        dcc.Markdown("""hello i'm tab two"""),
                        dcc.Markdown("""![country](./assets/images/tab2.jpg)"""),
                    ],
                ),
                dcc.Tab(
                    label="Tab three",
                    children=[
                        dcc.Markdown("""hello i'm tab two"""),
                        dcc.Markdown("""![sad girl](./assets/images/tab3.jpg)"""),
                    ],
                ),
            ]
        ),
        html.H1(
            children=dcc.Markdown(
                """

# This is an <h1> tag

## This is an <h2> tag

###### This is an <h6> tag

- list __elem__ 1
- list *elem* 2
- list elem 3

![alt text](./assets/images/sparkles.gif "Logo Title Text 1")

"""
            )
        ),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [
                    {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                    {
                        "x": [1, 2, 3],
                        "y": [2, 4, 5],
                        "type": "bar",
                        "name": u"Montréal",
                    },
                ],
                "layout": {"title": "Dash Data Visualization"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
