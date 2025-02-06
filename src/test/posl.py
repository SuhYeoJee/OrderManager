import sqlite3
import re

def get_possible_values_from_check_constraint(db_path, table_name, column_name):
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 테이블 정의를 가져오기 위한 쿼리
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    create_table_sql = cursor.fetchone()

    # 테이블이 존재하지 않으면 None 반환
    if create_table_sql is None:
        return f"테이블 '{table_name}'이(가) 존재하지 않습니다."

    create_table_sql = create_table_sql[0]

    # 주어진 컬럼의 CHECK 조건을 찾기 위한 정규 표현식
    check_constraint_pattern = re.compile(r"CHECK \(([^)]+)\)", re.IGNORECASE)

    # 테이블 생성 SQL에서 CHECK 제약 조건을 추출
    matches = check_constraint_pattern.findall(create_table_sql)
    
    possible_values = []
    for match in matches:
        # 해당 항목이 포함된 조건 찾기
        if column_name in match:
            # 'IN' 조건을 찾아서 사용 가능한 값 추출
            if 'IN' in match:
                values = re.findall(r"'([^']+)'", match)  # 작은따옴표로 감싸진 값들 추출
                possible_values = values
                break  # 한 번 찾으면 더 이상 검색할 필요 없음

    conn.close()

    # 사용 가능한 값 반환
    if possible_values:
        return possible_values
    else:
        return f"컬럼 '{column_name}'에 대한 CHECK 제약 조건을 찾을 수 없습니다."

# 사용 예시
db_path = 'example.db'  # 데이터베이스 파일 경로
table_name = 'A'  # 테이블 이름
column_name = 'B'  # 항목 이름

possible_values = get_possible_values_from_check_constraint(db_path, table_name, column_name)
print(f"{column_name} 항목에 사용 가능한 값: {possible_values}")
