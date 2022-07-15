#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def connect(login_host, login_port, login_user, login_password, auto_commit, trust_cert=True, database='master'):
    import sys
    import pyodbc

    boolyn = ('no','yes')

    login_string = login_host

    if login_port != "1433":
        login_string = "{login_host}:{login_port}".format(login_host=login_host, login_port=login_port)

    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+login_string+';DATABASE='+database+';UID='+login_user+';PWD='+login_password+';TrustServerCertificate='+boolyn[trust_cert], autocommit=auto_commit)
    except pyodbc.Error as e:
        sys.exit(str(e)+" Connection string: \
        DRIVER=ODBC Driver 18 for SQL Server;SERVER={login_string};DATABASE={database};UID={login_user};PWD={login_password};TrustServerCertificate=".format(login_string=login_string, login_user=login_user, login_password=login_password, database=database, trust_cert=trust_cert)+boolyn[trust_cert]+", autocommit={auto_commit}".format(auto_commit=auto_commit))
    return cnxn

def module_fail(module, msg, debug, secrets=[]):
    if os.environ.get('MODULE_DEBUGGING', 0):
        for secret in secrets:
            debug=debug.replace(secret, '****************')
        module.fail_json(msg=msg, changed=False, debug=debug)
    else:
        module.fail_json(msg=msg, changed=False)

def module_exit(module, msg, changed, debug, secrets=[]):
    if os.environ.get('MODULE_DEBUGGING', 0):
        for secret in secrets:
            debug=debug.replace(secret, '****************')
        module.exit_json(msg=msg, changed=changed, debug=debug)
    else:
        module.exit_json(msg=msg, changed=changed)