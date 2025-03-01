import pytest
from refactoring.db.SqliteQueryBuilder import SqliteQueryBuilder  # 네가 만든 모듈

@pytest.fixture
def sqb():
    """테스트용 메모리 DB 생성"""
    sqb = SqliteQueryBuilder()
    return sqb  # 테스트가 끝나면 db를 반환

@pytest.mark.parametrize(
    "table_name, column_value_pairs, expected",
    [
        ("users", {"id": 1, "name": "Alice"}, 
         ('INSERT INTO "users" ("id","name") VALUES (?,?);', [1, 'Alice'])),
        
        ("products", {"price": 99.99}, 
         ('INSERT INTO "products" ("price") VALUES (?);', [99.99])),
        
        ("logs", {}, 
         ('INSERT INTO "logs" () VALUES ();', []))  # 빈 값 테스트
    ]
)
def test_build_insert_query(sqb, table_name, column_value_pairs, expected):
    result = sqb.build_insert_query(table_name, column_value_pairs)
    assert result == expected


@pytest.mark.parametrize(
    "where, expected_where_clause, expected_bindings",
    [
        # 비교와 BETWEEN 조건을 결합한 예
        (
            {"comparison": [("column1", ">", 5), ("column2", "=", "val")],
             "between": [("column3", 10, 20)],
             "logic": '{comparisons[0]} AND {comparisons[1]} OR NOT {betweens[0]}'},  
            'WHERE "column1" > ? AND "column2" = ? OR NOT "column3" BETWEEN ? AND ?',
            [5, 'val', 10, 20]
        ),
        
        # IN 조건과 LIKE 조건을 결합한 예
        (
            {"inlist": [("column1", [1, 2, 3])], 
             "like": [("column2", "%pattern%")],
             "logic": '{inlists[0]} AND {likes[0]}'},
            'WHERE "column1" IN (?,?,?) AND "column2" LIKE ?',
            [1, 2, 3, '%pattern%']
        ),
        
        # IS NULL과 BETWEEN 조건을 결합한 예
        (
            {"isnull": [("column1", True), ("column2", False)], 
             "between": [("column3", 5, 10)],
             "logic": '{isnulls[0]} AND {betweens[0]}'},
            'WHERE "column1" IS NULL AND "column3" BETWEEN ? AND ?',
            [5, 10]
        ),
        
        # 여러 조건을 OR로 결합한 예
        (
            {"comparison": [("column1", ">", 10), ("column2", "<", 20)], 
             "logic": '{comparisons[0]} OR {comparisons[1]}'},
            'WHERE "column1" > ? OR "column2" < ?',
            [10, 20]
        ),

        # 하나의 조건만 있는 경우
        (
            {"comparison": [("column1", "=", 100)]},
            'WHERE "column1" = ?',
            [100]
        )
    ]
)
def test_build_where_clause(sqb, where, expected_where_clause, expected_bindings):
    where_clause, bindings = sqb._build_where_clause(where)
    assert where_clause == expected_where_clause
    assert bindings == expected_bindings
