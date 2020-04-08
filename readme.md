1. to start this project you gotta install [mysql](https://dev.mysql.com/doc/refman/8.0/en/mysql-installer-setup.html) 

    remember database name, username and password

1. clone this project via [http](https://github.com/annbgn/dash_app.git) or [ssh](git@github.com:annbgn/dash_app.git)

1. virtualenv

    ```python3 -m venv .```

1. requirements

    ```pip install pip-tools``` and ```pip install -r requirements\requirements.txt```

1. don't forget to replace DB_NAME, DB_USER and DB_PASSWORD with yours in connection_context_manager.py

1. run db_setup.py script

    ```python db_setup.py```
    
   if running into errors, try removing lines 64-65 indb_setup.py

1. now you are ready run app.py and check localhost in your browser

    ```python app.py```

have fun
