import pytest
from refactoring.db.DBManager import DBManager
from refactoring.db.params import *

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
        (InsertParams("users", {"id": 1, "name": "Alice"}), (1, "Alice")),

        # 다른 데이터 삽입
        (InsertParams("users", {"id": 2, "name": "Bob"}), (2, "Bob")),

        # 빈 문자열 삽입
        (InsertParams("users", {"id": 3, "name": ""}), (3, "")),

        # NULL 값 삽입 (id 자동 증가)
        (InsertParams("users", {"name": "Charlie"}), (1, "Charlie")),
    ]
)

def test_insert_record(new_dbm, test_input, expected):
    new_dbm.insert_record(test_input)
    result = new_dbm.select_records(SelectParams("users", ["id", "name"]))
    assert expected in result


@pytest.fixture
def dbm():
    dbm = DBManager("./test.db")
    dbm.db.execute_query("DROP TABLE IF EXISTS users")
    dbm.db.execute_query("CREATE TABLE users (id INTEGER PRIMARY KEY,name TEXT)")
    dbm.insert_record(InsertParams("users", {"id": 1, "name": "Alice"}))
    dbm.insert_record(InsertParams("users", {"id": 2, "name": "Bob"}))
    dbm.insert_record(InsertParams("users", {"id": 3, "name": ""}))
    dbm.insert_record(InsertParams("users", {"name": "Charlie"}))
    return dbm


@pytest.mark.parametrize(
    "test_input, expected",
    [
        # 기본적인 SELECT (모든 데이터 조회)
        (SelectParams("users", ["id", "name"]), [(1, "Alice"), (2, "Bob"), (3, ""), (4, "Charlie")]),

        # 특정 조건으로 SELECT (id=2인 데이터 조회)
        (SelectParams("users", ["id", "name"], WhereParams(comparison=[("id", "=", 2)])), [(2, "Bob")]),

        # SELECT 후 ORDER BY 적용
        (SelectParams("users", ["id", "name"], sort=SortParams("name", False)), [(3, ""), (1, "Alice"), (2, "Bob"),(4, "Charlie")]),

        # 특정 컬럼만 SELECT
        (SelectParams("users", ["id"]), [(1,), (2,), (3,), (4,)]),
    ]
)
def test_select_record(dbm, test_input, expected):
    result = dbm.select_records(test_input)
    assert result == expected