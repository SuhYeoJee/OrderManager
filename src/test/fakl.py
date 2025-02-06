import sqlite3
import re

def get_foreign_key_values(db_path, table_name, column_name):
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 테이블 정의를 가져오기 위한 쿼리
    cursor.execute("PRAGMA foreign_key_list(?)", (table_name,))
    foreign_keys = cursor.fetchall()

    # 테이블이 존재하지 않으면 None 반환
    if not foreign_keys:
        return f"테이블 '{table_name}'에 외래키 제약 조건이 없습니다."

    # 해당 외래키 찾기
    for fk in foreign_keys:
        if fk[4] == column_name:  # fk[4]는 외래키 컬럼 이름
            # 참조하는 테이블과 컬럼 정보
            ref_table = fk[2]
            ref_column = fk[4]

            # 참조하는 테이블의 값 조회
            cursor.execute(f"SELECT DISTINCT {ref_column} FROM {ref_table}")
            ref_values = cursor.fetchall()

            # 참조된 값들 반환
            return [value[0] for value in ref_values]

    conn.close()

    return f"컬럼 '{column_name}'에 대한 외래키 제약 조건을 찾을 수 없습니다."

# 사용 예시
db_path = 'example.db'  # 데이터베이스 파일 경로
table_name = 'A'  # 테이블 이름
column_name = 'B'  # 항목 이름

# 외래키 값 조회
foreign_key_values = get_foreign_key_values(db_path, table_name, column_name)
print(f"{column_name} 항목에 사용 가능한 외래키 값: {foreign_key_values}")
