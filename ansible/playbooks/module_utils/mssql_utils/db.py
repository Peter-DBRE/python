#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def db_exists(cnxn, cursor, db_name):
    try:
        cursor.execute("SELECT 1 FROM master.sys.databases WHERE name = 'db_name".format(db_name=db_name))
    except Exception as e:
        cnxn.rollback()
        sys.exit("error running cmd "+str(e))
    else:
        try:
            return_value=cursor.fetchval()
        except:
            return_value=0
        return_messages=cursor.messages
        cnxn.commit()
        if return_value == None:
            return_value=0
    return return_value#, return_messages

def db_create(cnxn, cursor, db_name, auto_commit):
    cnxn.autocommit = True
    try:
        cursor.execute("CREATE DATABASE [{db_name}];".format(db_name=db_name))
    except Exception as e:
        cnxn.rollback()
        sys.exit("error running cmd "+str(e))
    else:
        cnxn.commit()
        cnxn.autocommit = auto_commit
    return db_exists(cnxn, cursor, db_name)

def db_delete(cnxn, cursor, db_name):
    cnxn.autocommit = True
    try:
        cursor.execute("ALTER DAABASE [{db_name}] SET single_user WITH ROLLBACK IMMEDIATE".format(db_name=db_name))
        cursor.execute("DROP DATABASE [{db_name}];".format(db_name=db_name))
    except Exception as e:
        cnxn.rollback()
        sys.exit("error running cmd "+str(e))
    else:
        cnxn.commit()
        cnxn.autocommit = auto_commit
    return not db_exists(cnxn, cursor, db_name)