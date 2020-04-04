to start this project you gotta install mysql: https://dev.mysql.com/doc/refman/8.0/en/mysql-installer-setup.html 

create virtualenv, activate it, then 
```pip install pip-tools``` and ```pip-compile --output-file=requirements\requirements.txt requirements\requirements.in```


don't forget to replace DB_USER and DB_PASSWORD with yours in connection_context_manager.py and db_setup.py

run db_setup.py script

now you are ready run app.py and check localhost in your browser

have fun