import sqlite3

def get_foreign_key_values(db_path, table_name, column_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys = cursor.fetchall()

    result = {}
    for fk in foreign_keys:
        ref_table,col_name,ref_col = fk[2:5]

        # 참조 테이블에서 해당 컬럼의 모든 고유 값 가져오기
        query = f'SELECT DISTINCT "{ref_col}" FROM "{ref_table}"'
        ref_values = cursor.execute(query)
        result[col_name] = [x[0] for x in ref_values] if ref_values else []

    conn.close()
    return result if result else None

# 사용 예시
db_path = './config/NOVA.db'
table_name = 'orders' 
column_name = 'customer'
# 외래키 값 조회
foreign_key_values = get_foreign_key_values(db_path, table_name, column_name)
print(f"{column_name} 항목에 사용 가능한 외래키 값: {foreign_key_values}")
