#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION='''
---
module: mssql_db
'''
EXAMPLES = '''
#
'''
RETURN = '''
#
'''

import os
import sys
import pysnooper
import datetime
from io import StringIO

try:
    import pyodbc
except ImportError as e:
    py_imp_error = str(e)
    py_imp_fail = True
else:
    py_imp_fail = False

try:
    from ansible.module_utils.basic import AnsibleModule, missing_required_lib
except ImportError as e:
    ans_imp_error = str(e)
    ans_imp_fail = True
else:
    ans_imp_fail = False

try:
    from ansible.module_utils.mssql_utils import utils
except ImportError as e:
    msutils_imp_error = str(e)
    msutils_imp_fail = True
else:
    msutils_imp_fail = False

try:
    from ansible.module_utils.mssql_utils import db
except ImportError as e:
    msdb_imp_error = str(e)
    msdb_imp_fail = True
else:
    msdb_imp_fail = False

#setup pysnooper
sys.stderr = redirected_stderr = StringIO()
if not os.environ.get('MODULE_DEBUGGING'):
    os.environ["PYSNOOPER_DISABLED"] = "1"

@pysnooper.snoop(depth=2)
def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, aliases=['db_name']),
            login_user=dict(default=''),
            login_password=dict(default='', no_log=True),
            login_host=dict(required=True),
            login_port=dict(default='1433'),
            auto_commit=dict(type='bool', default=False),
            state=dict(
                default='present', choices=['present', 'absent'])
        )
    )

    db_name = module.params['name']
    state = module.params['state']
    auto_commit = module.params['auto_commit']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_host = module.params['login_host']
    login_port = module.params['login_port']

    cnxn = utils.connect(login_host, login_port, login_user, login_password, auto_commit, True, 'master')
    cursor = cnxn.cursor()

    if py_imp_fail:
        module.fail_json(msg="Failed to import package: "+str(py_imp_error))

    if ans_imp_fail:
        module.fail_json(msg="Failed to import package: "+str(ans_imp_error))

    if msutils_imp_fail:
        module.fail_json(msg="Failed to import package: "+str(msutils_imp_error))

    if msdb_imp_fail:
        module.fail_json(msg="Failed to import package: "+str(msdb_imp_error))

    if db.db_exists(cnxn, cursor, db_name):
        if state == 'absent':
            try:
                db.db_delete(cnxn, cursor, db_name, auto_commit)
            except Exception as e:
                utils.module_fail(module=module, msg="error deleting: "+str(e), debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])
            else:
                if db.db_exists(cnxn, cursor, db_name):
                    utils.module_fail(module=module, msg="error dropping db", debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])
                else:
                    utils.module_exit(module=module, msg='db dropped', changed=True, debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])
        elif state == 'present':
            utils.module_exit(module=module, msg='db exists', changed=False, debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])
    else:
        if state == 'present':
            try:
                db.db_create(cnxn, cursor, db_name, auto_commit)
            except Exception as e:
                utils.module_fail(module=module, msg="error creating database: "+str(e), debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])
            else:
                if db.db_exists(cnxn, cursor, db_name):
                    utils.module_exit(module=module, msg='db created', changed=True, debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])
                else:
                    utils.module_fail(module=module, msg="error creating db", debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])
                    
        elif state == 'absent':
            utils.module_exit(module=module, msg='db doesnt exist', changed=False, debug=redirected_stderr.getvalue(), secrets=[login_password, login_user])

if __name__ == '__main__':
    main()