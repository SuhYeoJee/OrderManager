import pytest
from refactoring.db.SqliteQueryBuilder import SqliteQueryBuilder
from refactoring.db.params import *

@pytest.fixture
def sqb():
    sqb = SqliteQueryBuilder()
    return sqb

# -------------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            WhereParam(
                comparison=[("column1", ">", 5), ("column2", "=", "val")],
                between=[("column3", 10, 20)],
                logic='{comparisons[0]} AND {comparisons[1]} OR NOT {betweens[0]}'
            ),
            ('WHERE "column1" > ? AND "column2" = ? OR NOT "column3" BETWEEN ? AND ?',
            [5, 'val', 10, 20])
        ),
        (
            WhereParam(
                comparison=[("columnA", "<", 100)],
                between=[("columnB", 50, 150)],
                logic='{comparisons[0]} OR NOT {betweens[0]}'
            ),
            ('WHERE "columnA" < ? OR NOT "columnB" BETWEEN ? AND ?',
            [100, 50, 150])
        ),
        (
            WhereParam(
                comparison=[("id", ">", 100)],
                like=[("name", "Alice%")],
                isnull=[("age", True)],
                logic='{comparisons[0]} AND {likes[0]} AND {isnulls[0]}'
            ),
            ('WHERE "id" > ? AND "name" LIKE ? AND "age" IS NULL',
            [100, 'Alice%'])
        ),
        (
            WhereParam(
                inlist=[("column1", [1, 2, 3])],
                logic='{inlists[0]}'
            ),
            ('WHERE "column1" IN (?,?,?)',
            [1, 2, 3])
        ),
        (
            WhereParam(
                comparison=[("id", "=", 123)],
                logic='{comparisons[0]}'
            ),
            ('WHERE "id" = ?',
            [123])
        ),
    ]
)

def test_build_where_clause(sqb,test_input, expected):
    where_clause = sqb._build_where_clause(test_input)
    assert where_clause == expected

# -------------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test_input, expected",
    [
        (SortParam(column_name="name", is_desc=True), 'ORDER BY "name" DESC'),
        (SortParam(column_name="name", is_desc=False), 'ORDER BY "name" ASC'),
        (SortParam(column_name="created_at", is_desc=True), 'ORDER BY "created_at" DESC'),
        (SortParam(column_name="created_at", is_desc=False), 'ORDER BY "created_at" ASC'),
        (SortParam(), 'ORDER BY "id" DESC'),
    ]
)

def test_build_sort_clause(sqb,test_input, expected):
    sort_clause = sqb._build_sort_clause(test_input)
    assert sort_clause == expected

# -------------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            InsertParam('users', {"id": 1, "name": "Alice"}),
            ('INSERT INTO "users" ("id","name") VALUES (?,?);', [1, 'Alice'])
        ),
        (
            InsertParam('products', {"product_id": 101, "price": 29.99}),
            ('INSERT INTO "products" ("product_id","price") VALUES (?,?);', [101, 29.99])
        ),
        (
            InsertParam('orders', {"order_id": 202, "order_date": QDate(2025, 3, 2)}),
            ('INSERT INTO "orders" ("order_id","order_date") VALUES (?,?);', [202, QDate(2025, 3, 2)])
        ),
        (
            InsertParam('events', {"event_id": 303, "event_time": QDateTime(2025, 3, 2, 12, 0)}),
            ('INSERT INTO "events" ("event_id","event_time") VALUES (?,?);', [303, QDateTime(2025, 3, 2, 12, 0)])
        ),
        (
            InsertParam('users', {"id": 4, "name": "Bob", "age": 30}),
            ('INSERT INTO "users" ("id","name","age") VALUES (?,?,?);', [4, 'Bob', 30])
        ),
    ]
)

def test_build_insert_query(sqb, test_input, expected):
    insert_query = sqb.build_insert_query(test_input)
    assert insert_query == expected

# -------------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            SelectParam(
                table_name="users",
                columns=["id", "name"],
                where=WhereParam(
                    comparison=[("id", ">", 10)],
                    logic='{comparisons[0]}'
                ),
                sort=SortParam("name", False)
            ),
            ('SELECT "id","name" FROM "users" WHERE "id" > ? ORDER BY "name" ASC;',
            [10])
        ),
        (
            SelectParam(
                table_name="orders",
                columns=["order_id", "order_date"],
                where=WhereParam(
                    comparison=[("order_id", "=", 100)],
                    logic='{comparisons[0]}'
                ),
                sort=SortParam("order_date", True)
            ),
            ('SELECT "order_id","order_date" FROM "orders" WHERE "order_id" = ? ORDER BY "order_date" DESC;',
            [100])
        ),
        (
            SelectParam(
                table_name="products",
                columns=["product_id", "price"],
                where=None,
                sort=None
            ),
            ('SELECT "product_id","price" FROM "products";',
            [])
        ),
        (
            SelectParam(
                table_name="customers",
                columns=["customer_id", "customer_name"],
                where=WhereParam(
                    inlist=[("customer_id", [1, 2, 3])],
                    logic='{inlists[0]}'
                ),
                sort=None
            ),
            ('SELECT "customer_id","customer_name" FROM "customers" WHERE "customer_id" IN (?,?,?);',
            [1, 2, 3])
        ),
        (
            SelectParam(
                table_name="employees",
                columns=["employee_id", "employee_name", "hire_date"],
                where=WhereParam(
                    comparison=[("hire_date", ">", QDate(2020, 1, 1))],
                    logic='{comparisons[0]}'
                ),
                sort=SortParam("employee_name", False)
            ),
            ('SELECT "employee_id","employee_name","hire_date" FROM "employees" WHERE "hire_date" > ? ORDER BY "employee_name" ASC;',
            [QDate(2020, 1, 1)])
        ),
    ]
)

def test_build_select_query(sqb, test_input, expected):
    select_query = sqb.build_select_query(test_input)
    assert select_query == expected

# -------------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test_input, expected",
    [
        # 단순한 업데이트 (WHERE 없음)
        (
            UpdateParam(
                table_name="users",
                column_value_pairs={"name": "Alice", "age": 30},
                where=None
            ),
            ('UPDATE "users" SET "name" = ?,"age" = ?;', ["Alice", 30])
        ),
        # WHERE 절 포함한 업데이트
        (
            UpdateParam(
                table_name="users",
                column_value_pairs={"age": 25},
                where=WhereParam(
                    comparison=[("id", "=", 1)],
                    logic='{comparisons[0]}'
                )
            ),
            ('UPDATE "users" SET "age" = ? WHERE "id" = ?;', [25, 1])
        ),
        # 여러 컬럼 업데이트 + WHERE 절 포함
        (
            UpdateParam(
                table_name="employees",
                column_value_pairs={"salary": 5000, "position": "Manager"},
                where=WhereParam(
                    comparison=[("employee_id", ">", 100)],
                    logic='{comparisons[0]}'
                )
            ),
            ('UPDATE "employees" SET "salary" = ?,"position" = ? WHERE "employee_id" > ?;', [5000, "Manager", 100])
        ),
        # 날짜 데이터 포함
        (
            UpdateParam(
                table_name="tasks",
                column_value_pairs={"due_date": QDate(2025, 5, 20)},
                where=WhereParam(
                    comparison=[("status", "=", "pending")],
                    logic='{comparisons[0]}'
                )
            ),
            ('UPDATE "tasks" SET "due_date" = ? WHERE "status" = ?;', [QDate(2025, 5, 20), "pending"])
        ),
    ]
)
def test_build_update_query(sqb, test_input, expected):
    update_query = sqb.build_update_query(test_input)
    assert update_query == expected

# -------------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test_input, expected",
    [
        # WHERE 조건을 사용하는 경우
        (
            DeleteParam(
                table_name="users",
                where=WhereParam(
                    comparison=[("id", "=", 1)],
                    logic='{comparisons[0]}'
                )
            ),
            ('DELETE FROM "users" WHERE "id" = ?;', [1])
        ),
        # column_value_pairs를 사용하는 경우 (가장 큰 id 삭제)
        (
            DeleteParam(
                table_name="users",
                column_value_pairs={"name": "Alice", "age": 30}
            ),
            ('DELETE FROM "users" WHERE id = (SELECT MAX(id) FROM users WHERE "name" = ? AND "age" = ?);', ["Alice", 30])
        ),
        # WHERE 조건이 복합적인 경우
        (
            DeleteParam(
                table_name="employees",
                where=WhereParam(
                    comparison=[("salary", "<", 3000)],
                    logic='{comparisons[0]}'
                )
            ),
            ('DELETE FROM "employees" WHERE "salary" < ?;', [3000])
        ),
        # 날짜 필터링을 사용하는 경우
        (
            DeleteParam(
                table_name="tasks",
                column_value_pairs={"due_date": QDate(2025, 5, 20)}
            ),
            ('DELETE FROM "tasks" WHERE id = (SELECT MAX(id) FROM tasks WHERE "due_date" = ?);', [QDate(2025, 5, 20)])
        ),
    ]
)
def test_build_delete_query(sqb,test_input, expected):
    delete_query = sqb.build_delete_query(test_input)
    assert delete_query == expected
