def test_db(ansible_module):
    name="testdb1"
    login_user="sa"
    login_host="localhost"
    state="present"
    contacted = ansible_module.mssql_db_demo()

    for (host, result) in contacted.items():
        assert 'failed' not in result, result['msg']
        assert 'changed' in result

    name="testdb1"
    login_user="sa"
    login_host="localhost"
    state="absent"
    contacted = ansible_module.mssql_db_demo()

    for (host, result) in contacted.items():
        assert 'failed' not in result, result['msg']
        assert 'changed' in result