import pytest
from refactoring.db import DBManager,InsertParam,SelectParam,UpdateParam,DeleteParam,WhereParam,SortParam

@pytest.fixture
def new_dbm():
    dbm = DBManager("./test.db")
    dbm.db.execute_query("DROP TABLE IF EXISTS users")
    dbm.db.execute_query("CREATE TABLE users (id INTEGER PRIMARY KEY,name TEXT)")
    return dbm

@pytest.mark.parametrize(
    "test_input, expected",
    [
        # 기본적인 데이터 삽입
        (InsertParam("users", {"id": 1, "name": "Alice"}), ({'id':1, 'name':"Alice"})),

        # 다른 데이터 삽입
        (InsertParam("users", {"id": 2, "name": "Bob"}), ({'id':2, 'name':"Bob"})),

        # 빈 문자열 삽입
        (InsertParam("users", {"id": 3, "name": ""}), ({'id':3, 'name':""})),

        # NULL 값 삽입 (id 자동 증가)
        (InsertParam("users", {"name": "Charlie"}), ({'id':1, 'name':"Charlie"})),
    ]
)

def test_insert_record(new_dbm, test_input, expected):
    new_dbm.insert_record(test_input)
    result = new_dbm.select_records(SelectParam("users", ["id", "name"]))
    assert expected in result

# -------------------------------------------------------------------------------------------

@pytest.fixture
def dbm():
    dbm = DBManager("./test.db")
    dbm.db.execute_query("DROP TABLE IF EXISTS users")
    dbm.db.execute_query("CREATE TABLE users (id INTEGER PRIMARY KEY,name TEXT)")
    dbm.insert_record(InsertParam("users", {"id": 1, "name": "Alice"}))
    dbm.insert_record(InsertParam("users", {"id": 2, "name": "Bob"}))
    dbm.insert_record(InsertParam("users", {"id": 3, "name": ""}))
    dbm.insert_record(InsertParam("users", {"name": "Charlie"}))
    return dbm


@pytest.mark.parametrize(
    "test_input, expected",
    [
        # 기본적인 SELECT (모든 데이터 조회)
        (SelectParam("users", ["id", "name"]), [{'id':1, 'name':"Alice"}, {'id':2, 'name':"Bob"}, {'id':3, 'name':""}, {'id':4, 'name':"Charlie"}]),

        # 특정 조건으로 SELECT (id=2인 데이터 조회)
        (SelectParam("users", ["id", "name"], WhereParam(comparison=[("id", "=", 2)])), [{'id':2, 'name':"Bob"}]),

        # SELECT 후 ORDER BY 적용
        (SelectParam("users", ["id", "name"], sort=SortParam("name", False)), [{'id':3, 'name':""},{'id':1, 'name':"Alice"}, {'id':2, 'name':"Bob"},  {'id':4, 'name':"Charlie"}]),

        # 특정 컬럼만 SELECT
        (SelectParam("users", ["id"]), [{'id':1},{'id':2},{'id':3},{'id':4}]),
    ]
)
def test_select_record(dbm, test_input, expected):
    result = dbm.select_records(test_input)
    assert result == expected

@pytest.mark.parametrize("test_input, expected", [
    (UpdateParam("users", {"name": "Updated Name"}, WhereParam(comparison=[("id", "=", 2)])), [{'id':2, 'name':"Updated Name"}]),
    (UpdateParam("users", {"name": "New Alice"}, WhereParam(comparison=[("id", "=", 1)])), [{'id':1, 'name':"New Alice"}]),
    (UpdateParam("users", {"name": "Anonymous"}, WhereParam(comparison=[("id", "=", 3)])), [{'id':3, 'name':"Anonymous"}]),
])
def test_update_record(dbm, test_input, expected):
    dbm.update_record(test_input)
    result = dbm.select_records(SelectParam("users", ["id", "name"],WhereParam(comparison=[("id", "=", test_input.where.comparison[0][2])])))
    assert result == expected

@pytest.mark.parametrize("test_input, expected", [
    (DeleteParam("users", where=WhereParam(comparison=[("id", "=", 2)])), [1, 3, 4]),
    (DeleteParam("users", where=WhereParam(comparison=[("name", "=", "Alice")])), [2, 3, 4]),
    (DeleteParam("users", where=WhereParam(comparison=[("id", ">", 1)])), [1]),
])
def test_delete_record(dbm, test_input, expected):
    dbm.delete_record(test_input)
    result = [row['id'] for row in dbm.select_records(SelectParam("users", ["id"]))]
    assert sorted(result) == sorted(expected)

# -------------------------------------------------------------------------------------------

def test_get_table_names(dbm):
    result = dbm.get_table_names()
    assert 'users' in result

def test_get_table_ids(dbm):
    result = dbm.get_table_ids('users')
    assert result == [1,2,3,4]

def test_get_table_col_names(dbm):
    result = dbm.get_table_col_names('users')
    assert result == ['id','name']

def test_get_table_col_type(dbm):
    result = dbm.get_table_col_type('users','name')
    assert result == 'TEXT'

def test_select_records_by_comparison(dbm):
    result = dbm.select_records_by_comparison('users','name','Bob')
    assert result == [{'id': 2, 'name': 'Bob'}]