import mysql.connector
from mysql.connector.errors import ProgrammingError

from connection_context_manager import (
    ConnectionManager,
    DB_NAME,
    DB_PASSWORD,
    DB_USER,
    DB_HOST,
)


def create_db():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        auth_plugin="mysql_native_password",
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE {}".format(DB_NAME))


def create_tables():
    user_sql = """CREATE TABLE user (user_id integer, name varchar(255));"""
    task_sql = """CREATE TABLE task (task_id integer, user_id integer, text varchar(1024), is_done boolean, tags varchar(255), due date);"""
    subtask_sql = """CREATE TABLE subtask (subtask_id integer, task_id integer, user_id integer, text varchar(1024), is_done boolean);"""
    with ConnectionManager() as cm:
        for sql in [user_sql, task_sql, subtask_sql]:
            try:
                cm.cursor.execute(sql)
            except ProgrammingError as e:
                print(e)


def db_fill_initial_data():
    user_sql = """INSERT INTO user (user_id, name) VALUES (1, "Anna");"""
    task_sql_1 = """INSERT INTO task (task_id, user_id, text, is_done, tags, due) VALUES (1, 1, "movie marathon night", FALSE, "#entertaiment #movies", "2020-04-11");"""
    task_sql_2 = """INSERT INTO task (task_id, user_id, text, is_done, tags, due) VALUES (2, 1, "cook the dinner", TRUE, "#food", CURDATE());"""
    subtask_sql_1 = """INSERT INTO subtask (subtask_id, task_id, user_id, text, is_done) VALUES (1, 1, 1, "only lovers left alive -- jim jarmush", TRUE);"""
    subtask_sql_2 = """INSERT INTO subtask (subtask_id, task_id, user_id, text, is_done) VALUES (2, 1, 1, "7 samurai -- akira kurosava", TRUE);"""
    subtask_sql_3 = """INSERT INTO subtask (subtask_id, task_id, user_id, text, is_done) VALUES (3, 1, 1, "vertigo -- alfred hitchhock", TRUE);"""
    subtask_sql_4 = """INSERT INTO subtask (subtask_id, task_id, user_id, text, is_done) VALUES (4, 1, 1, "some like it hot", TRUE);"""
    subtask_sql_5 = """INSERT INTO subtask (subtask_id, task_id, user_id, text, is_done) VALUES (5, 1, 1, "how i stopped worring and loved the bobm -- stanley kubrick", TRUE);"""
    subtask_sql_6 = """INSERT INTO subtask (subtask_id, task_id, user_id, text, is_done) VALUES (6, 2, 1, "go shopping", TRUE);"""
    subtask_sql_7 = """INSERT INTO subtask (subtask_id, task_id, user_id, text, is_done) VALUES (7, 2, 1, "actually cook the meal", TRUE);"""

    sqls = [
        user_sql,
        task_sql_1,
        task_sql_2,
        subtask_sql_1,
        subtask_sql_2,
        subtask_sql_3,
        subtask_sql_4,
        subtask_sql_5,
        subtask_sql_6,
        subtask_sql_7,
    ]

    with ConnectionManager() as cm:
        for sql in sqls:
            try:
                cm.cursor.execute(sql)
            except ProgrammingError as e:
                print(e)


if __name__ == "__main__":
    create_db()
    print("database {} created successfully".format(DB_NAME))

    create_tables()
    print("tables crated successfully")

    show_sql = "SHOW TABLES FROM {};".format(DB_NAME)
    with ConnectionManager() as cm:
        cm.cursor.execute(show_sql)

    db_fill_initial_data()
    print("database filled")

    print("setup finished")
