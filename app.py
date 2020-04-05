# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from connection_context_manager import ConnectionManager


def get_db_data():
    result = {}
    sql_select_tasks = """SELECT DISTINCT task_id FROM task LIMIT 10;"""
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
            result.update({task[0]: subtask_dict})
    return result


def generate_tables():
    children = []
    for task, subtasks_list in get_db_data().items():
        children.append(
            dash_table.DataTable(
                id="table{}".format(str(task)),
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
        "marker": {"color": "palegreen"},
    }
    undone = {
        "x": [day.strftime("%a, %d %b %Y") for day in upcoming_week],
        "y": [amount[0] for amount in count_undone],
        "type": "bar",
        "name": "undone",
        "marker": {"color": "lightcoral"},
    }

    graph = dcc.Graph(
        id="proportion_chart",
        figure={
            "data": [done, undone],
            "layout": {"title": "Proportion of done and not (yet) done tasks, splitted by due date",},
        },
    )
    return graph


if __name__ == "__main__":
    local_stylesheets = ["./assets/styles.css"]
    app = dash.Dash(__name__, external_stylesheets=local_stylesheets)
    app.layout = html.Div(
        dcc.Tabs(
            [
                dcc.Tab(label="Tasks", children=generate_tables()),
                dcc.Tab(label="Chart", children=[get_bar_chart()],),
            ]
        )
    )

    app.run_server(debug=True)
