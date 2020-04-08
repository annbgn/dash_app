# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from connection_context_manager import ConnectionManager


def get_db_data():
    result = {}
    sql_select_tasks = """SELECT DISTINCT task_id, text FROM task LIMIT 10;"""
    with ConnectionManager() as cm:
        cm.cursor.execute(sql_select_tasks)
        tasks_result = cm.cursor.fetchall()  # list of tuples, e.g. [(1,), (2,)]
        for task in tasks_result:
            sql_select_subtask = """SELECT DISTINCT subtask_id, text, is_done FROM subtask WHERE task_id ={} LIMIT 10;""".format(
                task[0]
            )
            cm.cursor.execute(sql_select_subtask)
            subtask_result = cm.cursor.fetchall()
            subtask_dict = [
                {"text": subtask[1], "is_done": subtask[2]}
                for subtask in subtask_result
            ]
            result.update({(task[0], task[1]): subtask_dict})
    return result


def generate_tables():
    children = []
    for task, subtasks_list in get_db_data().items():
        children.append(html.H4(str(task[1])))
        children.append(
            dash_table.DataTable(
                id="table{}".format(str(task[0])),
                columns=[
                    {"name": "text", "id": "text"},
                    {"name": "is_done", "id": "is_done"},
                ],
                data=[
                    {
                        "text": subtask["text"],
                        "is_done": "true" if subtask["is_done"] else "false",
                    }
                    for subtask in subtasks_list
                ],
                style_cell={"textAlign": "left"},
                editable=True,
                row_deletable=True,
            ),
        )
        children.append(
            html.Button(
                "Add Row",
                id="add_button{}".format(str(task[0])),
                n_clicks=0,
                className="example_d",
            )
        )
    return children


def get_bar_chart():
    upcoming_week = [datetime.today() + timedelta(days=i) for i in range(7)]
    sql_done = [
        """SELECT COUNT(*) FROM task WHERE is_done=1 AND due="{}";""".format(
            day.strftime("%Y-%m-%d")
        )
        for day in upcoming_week
    ]
    sql_undone = [
        """SELECT COUNT(*) FROM task WHERE is_done=0 AND due="{}";""".format(
            day.strftime("%Y-%m-%d")
        )
        for day in upcoming_week
    ]
    count_done = []
    count_undone = []
    with ConnectionManager() as cm:
        for sql in sql_done:
            cm.cursor.execute(sql)
            count_done += [cm.cursor.fetchone()]
        for sql in sql_undone:
            cm.cursor.execute(sql)
            count_undone += [cm.cursor.fetchone()]
    done = {
        "x": [day.strftime("%a, %d %b %Y") for day in upcoming_week],
        "y": [amount[0] for amount in count_done],
        "type": "bar",
        "name": "done",
        "marker": {"color": "MediumAquamarine"},
    }
    undone = {
        "x": [day.strftime("%a, %d %b %Y") for day in upcoming_week],
        "y": [amount[0] for amount in count_undone],
        "type": "bar",
        "name": "undone",
        "marker": {"color": "PaleVioletRed"},
    }

    graph = dcc.Graph(
        id="proportion_chart",
        figure={
            "data": [done, undone],
            "layout": {
                "title": "Proportion of done and not (yet) done tasks, splitted by due date",
            },
        },
    )
    return graph


def get_md():
    md = """
### Say Hi to your new todo list manager!
#### Features:

- tasks with subtasks
- visualize upcoming due dates
- cool singlepage design = no redirects & loadings
- it's an open source studying project ([github](https://github.com/annbgn/dash_app))
"""
    return md


def register_callbacks(app):
    for task, subtasks_list in get_db_data().items():

        @app.callback(
            Output("table{}".format(str(task[0])), "data"),
            [Input("add_button{}".format(str(task[0])), "n_clicks")],
            [
                State("table{}".format(str(task[0])), "data"),
                State("table{}".format(str(task[0])), "columns"),
            ],
        )
        def add_row(n_clicks, rows, columns):
            if n_clicks > 0:
                rows.append({c["id"]: "" for c in columns})
            return rows

    @app.callback(
        dash.dependencies.Output("dd-output-container", "children"),
        [dash.dependencies.Input("demo-dropdown", "value")],
    )
    def update_output(value):
        return 'You have selected "{}"'.format(value)

    @app.callback(
        Output("textarea-example-output", "children"),
        [Input("textarea-example", "value")],
    )
    def update_output(value):
        return "You have entered: \n{}".format(value)


def get_optional_elements():
    style = {"color": "white", "font-family": "verdana", "font-size": "20px"}
    children = []
    children += [
        html.P("How did you like the site?", style=style),
        dcc.Dropdown(
            id="demo-dropdown",
            options=[
                {"label": "great", "value": "great"},
                {"label": "gorgeous", "value": "gorgeous"},
                {"label": "magnificent", "value": "magnificent"},
            ],
            value="",
        ),
        html.Div(id="dd-output-container"),
    ]
    children += [
        html.P("Leave a comment if you like", style=style),
        dcc.Textarea(
            id="textarea-example",
            value="Feedback\nmakes us being better",
            style={"width": "100%", "height": 300},
        ),
        html.Div(id="textarea-example-output", style={"whiteSpace": "pre-line"}),
    ]

    return children


if __name__ == "__main__":
    local_stylesheets = ["./assets/styles.css"]
    app = dash.Dash(__name__, external_stylesheets=local_stylesheets)
    app.config.suppress_callback_exceptions = True

    app.title = "TO DO list"
    app.layout = html.Div(
        children=[
            html.H1("Aim High", id="main_header"),
            dcc.Markdown(get_md(), style={"color": "white", "font-size": "20px"}),
            dcc.Tabs(
                [
                    dcc.Tab(label="Tasks", children=generate_tables()),
                    dcc.Tab(label="Chart", children=[get_bar_chart()],),
                ]
            ),
            html.Div(children=get_optional_elements()),
            html.Footer(
                children=[
                    html.P(
                        "2020, Anna Bogdanova",
                        style={
                            "color": "Turquoise",
                            "font-family": "Verdana",
                            "font-size": "15px",
                            "vertical-align": "middle",
                        },
                    )
                ]
            ),
        ]
    )

    register_callbacks(app)

    app.run_server(debug=True)
