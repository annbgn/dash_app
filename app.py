# -*- coding: utf-8 -*-

from connection_context_manager import ConnectionManager
import mysql.connector

import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html

import sqlite3
from sqlite3 import Error


def get_db_data():
    result = {}
    sql_select_tasks = """SELECT task_id FROM task LIMIT 5;"""
    with ConnectionManager() as cm:
        cm.cursor.execute(sql_select_tasks)
        tasks_result = cm.cursor.fetchall()  # list of tuples, e.g. [(1,), (2,)]
        for task in tasks_result:
            sql_select_subtask = """SELECT subtask_id, text, is_done FROM subtask WHERE task_id ={} LIMIT 5;""".format(
                task[0]
            )
            cm.cursor.execute(sql_select_subtask)
            subtask_result = cm.cursor.fetchall()
            subtask_dict = [
                {"text": subtask[1], "is_done": subtask[2]}
                for subtask in subtask_result
            ]
            result.update({task[0]: subtask_dict})
    # print(result)
    return result


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
local_stylesheets = ["./assets/styles.css"]
app = dash.Dash(__name__, external_stylesheets=local_stylesheets)

# table_data = get_db_data()
'''app.layout = html.Div(
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
        dcc.Dropdown(
            id="demo-dropdown",
            options=[
                {"label": "New York City", "value": "NYC"},
                {"label": "Montreal", "value": "MTL"},
                {"label": "San Francisco", "value": "SF"},
            ],
            value="NYC",
        ),
        html.Div(id="dd-output-container"),
        dash_table.DataTable(
            id="table",
            columns=[
                {"name": "purchase_id", "id": str(1)},
                {"name": "user", "id": str(2)},
                {"name": "price", "id": str(3)},
            ],
            data=table_data,
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
'''

def generate_tables():
    children = []
    for task, subtasks_list in get_db_data().items():
        # import pdb;pdb.set_trace()
        children.append(
            dash_table.DataTable(
                id="table{}".format(str(task)),
                columns=[{"name": "text", "id": "text"},
                         {"name": "is_done", "id": "is_done"}
                         ],
                data=[
                    {
                        "text": subtask["text"],
                        "is_done": "true" if subtask["is_done"] else "false",
                    }
                    for subtask in subtasks_list
                ],
            )
        )
    return children
app.layout = html.Div(children=generate_tables())

'''
@app.callback(
    dash.dependencies.Output("dd-output-container", "children"),
    [dash.dependencies.Input("demo-dropdown", "value")],
)
def update_output(value):
    return 'You have selected "{}"'.format(value)
'''

if __name__ == "__main__":
    app.run_server(debug=True)
