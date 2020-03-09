# -*- coding: utf-8 -*-
import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    else:

        cursor = conn.cursor()

        sql_create_table = """CREATE TABLE purchases (purchase_id int, user varchar(255), price float(255, 7));"""
        cursor.execute(sql_create_table)

        conn.commit()
    finally:
        if conn:
            conn.close()


def add_purchase():
    conn = db_connect()
    cursor = conn.cursor()
    sql_add = """INSERT INTO purchases (purchase_id, user, price)
VALUES (1, "William", 100);"""
    cursor.execute(sql_add)
    conn.commit()
    db_connection_close(conn)


def db_connect():  # -> conneсtion
    conn = None
    try:
        conn = sqlite3.connect(r"D:\databases_for_university\dashdb\pythonsqlite.db")
        # import pdb;pdb.set_trace()
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def db_connection_close(conn):
    if conn:
        conn.close()


def get_db_data():
    conn = db_connect()
    cursor = conn.cursor()
    sql_select = """SELECT * FROM purchases;"""
    cursor.execute(sql_select)
    result = cursor.fetchall()
    for r in result:
        print(r)
    db_connection_close(conn)
    return result


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
local_stylesheets = ["./assets/styles.css"]
app = dash.Dash(__name__, external_stylesheets=local_stylesheets)

table_data = get_db_data()
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
        dcc.Dropdown(
            id="demo-dropdown",
            options=[
                {"label": "New York City", "value": "NYC"},
                {"label": "Montreal", "value": "MTL"},
                {"label": "San Francisco", "value": "SF"},
            ],
            value="NYC",
        ),
        dash_table.DataTable(
            id="table",
            columns=[
                {"name": "purchase_id", "id": str(1)},
                {"name": "user", "id": str(2)},
                {"name": "price", "id": str(3)},
            ],
            data=[
                {"purchase_id": t[0], "user": t[1], "price": t[2]} for t in table_data
            ],
        ),
        html.Div(id="dd-output-container"),
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


@app.callback(
    dash.dependencies.Output("dd-output-container", "children"),
    [dash.dependencies.Input("demo-dropdown", "value")],
)
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == "__main__":
    # create_connection(r"D:\databases_for_university\dashdb\pythonsqlite.db")
    # add_purchase()

    app.run_server(debug=True)
