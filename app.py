# -*- coding: utf-8 -*-

import dash
import dash_html_components as html
import dash_table

from connection_context_manager import ConnectionManager


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
            )
        )
    return children


if __name__ == "__main__":
    local_stylesheets = ["./assets/styles.css"]
    app = dash.Dash(__name__, external_stylesheets=local_stylesheets)
    app.layout = html.Div(children=generate_tables())

    app.run_server(debug=True)
