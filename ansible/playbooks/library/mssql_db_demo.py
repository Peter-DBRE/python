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
import pyodbc

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

from ansible.module_utils.mssql_utils import utils
from ansible.module_utils.mssql_utils import db



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

bools = ('no', 'yes')

cnxn = utils.connect(login_host, login_port, login_user, login_password, auto_commit, 'master')
cursor = cnxn.cursor()

return_vault=None

changed = False
if db_exists(cnxn, cursor, db_name):
    if state == 'absent':
        try:
            changed = db_delete(cnxn, cursor, db_name, auto_commit)
        except Exception as e:
            module.fail_json(msg="error deleting: "+str(e))
        else:
            module.exit_json(changed=changed, db_name=db_name)
    elif state == 'present':
        try:
            changed = db_create(cnxn, cursor, db_name, auto_commit)
        except Exception as e:
            module.fail_json(msg="error creating database: "+str(e))

    module.exit_json(changed=changed, db_name=db_name)

if __name__ == '__main__':
    main()