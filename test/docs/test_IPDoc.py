import pytest
from refactoring.docs.IPDoc import *
from refactoring.docs.params import *

CREATE_ITEM_TABLE = '''CREATE TABLE item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    segment1_name TEXT REFERENCES segment(name),
    segment1_amount INTEGER,
    segment2_name TEXT REFERENCES segment(name),
    segment2_amount INTEGER,
    shank_name TEXT REFERENCES shank(name),
    shank_amount INTEGER,
    submaterial1_name TEXT REFERENCES submaterial(name),
    submaterial1_amount INTEGER,
    submaterial2_name TEXT REFERENCES submaterial(name),
    submaterial2_amount INTEGER
);'''

CREATE_IP_TABLE = '''CREATE TABLE ip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);'''

@pytest.fixture
def dbm():
    dbm = DBManager("./test.db")
    dbm.db.execute_query("DROP TABLE IF EXISTS item")
    dbm.db.execute_query("DROP TABLE IF EXISTS ip")
    dbm.db.execute_query(CREATE_ITEM_TABLE)
    dbm.db.execute_query(CREATE_IP_TABLE)
    dbm.insert_record(InsertParam("item", 
                                  {"name": "TEST-G1 A",
                                    "segment1_name": "SQTEST1",
                                    "segment1_amount": 3,
                                    "shank_name":"DBS-CCW",
                                    "shank_amount": 1,
                                    "submaterial1_name": "PCD10",
                                    "submaterial1_amount": 1
                                   }))
    dbm.insert_record(InsertParam("item", 
                                  {"name": "TEST-G2 A",
                                    "segment1_name": "SQTEST1",
                                    "segment1_amount": 1,
                                    "segment2_name": "SQTEST2",
                                    "segment2_amount": 2,
                                    "shank_name":"SQ948-CW",
                                    "shank_amount": 1,
                                    "submaterial1_name": "PCD10",
                                    "submaterial1_amount": 1,
                                    "submaterial2_name": "PCD12",
                                    "submaterial2_amount": 2,
                                   }))
    return dbm


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (IPDocItemParam("TEST-G1 A", 1), '2025-IP0001'),
    ]
)

def test_build_ip(dbm, test_input, expected):
    ipd = IPDoc(dbm,IPDocParam(item1=test_input))
    result = ipd.name
    assert expected in result