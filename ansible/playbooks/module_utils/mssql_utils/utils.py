#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def connect(login_host, login_port, login_user, login_password, auto_commit, database='master'):
    import sys
    import pyodbc

    boolyn = ('no','yes')

    login_string = login_host

    if login_port != "1433":
        login_string = "{login_host}:{login_port}".format(login_host=login_host, login_port=login_port)

    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+login_string+';DATABASE='+database+';UID='+login_user+';PWD='+login_password, autocommit=auto_commit)
    except pyodbc.Error as e:
        sys.exit(str(e)+" Connection string: \
        DRIVER=ODBC Driver 18 for SQL Server;SERVER={login_string};DATABASE={database};UID={login_user};PWD={login_password}, autocommit={auto_commit}".format(login_string=login_string, login_user=login_user, login_password=login_password, auto_commit=auto_commit))
    return cnxn