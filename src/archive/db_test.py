import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# 테이블 생성
# cursor.execute('''
# CREATE TABLE my_table (
#     id INTEGER PRIMARY KEY,
#     data TEXT,
#     reg_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- 생성 날짜 자동 저장
#     update_date DATETIME DEFAULT CURRENT_TIMESTAMP -- 수정 날짜 기본값
# );

# ''')

cursor.execute('''
CREATE TRIGGER update_date_trigger
AFTER UPDATE ON my_table
BEGIN
    UPDATE my_table
    SET update_date = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;
''')


# # 데이터 삽입
# cursor.execute("INSERT INTO my_table (data) VALUES ('Alice')")
# cursor.execute("INSERT INTO my_table (data) VALUES ('Busan')")
cursor.execute("UPDATE my_table SET data = 'Tom' WHERE id = 1")


# 데이터 조회
cursor.execute("SELECT * FROM my_table")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 변경 사항 저장
conn.commit()

# 연결 종료
conn.close()