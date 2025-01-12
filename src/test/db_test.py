import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# # 테이블 생성
# cursor.execute('''
#     CREATE TABLE users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         age TEXT,
#         city TEXT
#     )
# ''')

# # # 데이터 삽입
# cursor.execute("INSERT INTO users (name, age, city) VALUES ('Alice', '30', 'Seoul')")
# cursor.execute("INSERT INTO users (name, age, city) VALUES ('Bob', '25', 'Busan')")


# 데이터 조회
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 변경 사항 저장
conn.commit()

# 연결 종료
conn.close()