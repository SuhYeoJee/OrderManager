


class QueryBuilder():
    def __init__(self):
        ...

    def _get_double_quotes_str(self,item)->str:
        '''쌍따옴표로 감싼 문자열 반환 '''
        return f'''"{str(item)}"'''

    def get_insert_query(self,table_name:str,items:dict)->str:
        '''INSERT INTO 테이블명 (키1, 키2, ...) VALUES (값1, 값2, ...);'''
        return f'''INSERT INTO "{table_name}" ({",".join(map(self._get_double_quotes_str,items.keys()))}) VALUES ({",".join(map(self._get_double_quotes_str,items.values()))});'''
    
    def _get_where_str(self)->str:
        '''
        kwargs 받는게 낫지 않을까

        비교: >,<,=,!=,>=,<=
            [(컬럼,연산자,값)]
        구간: BETWEEN ... AND ...
            [(컬럼,시작값,끝값)]
        일치목록: IN (...)
            [(컬럼,[목록])]
        패턴검색: LIKE
            [(컬럼,패턴)]
        널일치: IS NULL / IS NOT NULL
            [(컬럼,True(값 존재)),(컬럼,False(값 부재))]

        이 조건식들을 어떻게 논리 연결할지가 문제임.. 
        논리: AND, OR, NOT
            이거는 조건식에 붙여야함
        
        조건식 논리를 스트링으로 받을까
        '{a[0]} AND {a[1]} OR NOT {b[0]}'.format(a = [1,2],b=[3])
        
        '''

        print('{a[0]} AND {a[1]} OR NOT {b[0]}'.format(a = [1,2],b=[3]))
        
    
if __name__ == '__main__':
    qb = QueryBuilder()
    res = qb.get_insert_query('users',{'name':'Tom','age':23,'city':'Seoul'})
    print(res)