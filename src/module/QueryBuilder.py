
class QueryBuilder():
    def __init__(self):...
    # --------------------------
    def _get_stred_item(self,item)->str:
        '''문자열로 바꿔서 반환, 필요한경우 "를 추가함'''
        return f'''"{item}"''' if isinstance(item,str) else f'''{str(item)}'''
    # --------------------------
    def _get_where_str(self,logic_str:str='',**kwargs)->str:
        '''
        comparison: >,<,=,!=,>=,<=
            [(컬럼,연산자,값)]
        between: BETWEEN ... AND ...
            [(컬럼,시작값,끝값)]
        inlist: IN (...)
            [(컬럼,[목록])]
        likepattern: LIKE
            [(컬럼,패턴)]
        isnull: IS NULL / IS NOT NULL
            [(컬럼,True(값 존재)),(컬럼,False(값 부재))]

        조건식 논리를 스트링으로 입력 (기본: AND 연결)
        논리: AND, OR, NOT
        logic_str = '{comparison[0]} AND {comparison[1]} OR NOT {between[0]}'
        '''
        comparison = []
        if 'comparison' in kwargs.keys():
            for i in kwargs['comparison']:
                col,op,val = i
                comparison.append(f'''{self._get_stred_item(col)} {op} {self._get_stred_item(val)}''')

        between = []
        if 'between' in kwargs.keys():
            for i in kwargs['between']:
                col,start,end = i
                between.append(f'''{self._get_stred_item(col)} BETWEEN {self._get_stred_item(start)} AND {self._get_stred_item(end)}''')

        inlist = []
        if 'inlist' in kwargs.keys():
            for i in kwargs['inlist']:
                col,vals = i
                inlist.append(f'''{self._get_stred_item(col)} IN ({', '.join(map(self._get_stred_item,vals))})''')

        likepattern = [] 
        if 'likepattern' in kwargs.keys():
            for i in kwargs['likepattern']:
                col,pattern = i
                likepattern.append(f'''{self._get_stred_item(col)} LIKE {self._get_stred_item(pattern)}''')
        
        isnull = []
        if 'isnull' in kwargs.keys():
            for i in kwargs['isnull']:
                col,flag = i
                isnull.append(f'''{self._get_stred_item(col)} IS {'' if flag else 'NOT'} NULL''')
        # -------------------------------------------------------------------------------------------
        if not logic_str:
            res = 'WHERE ' + ' AND '.join (comparison+between+inlist+likepattern+isnull)
        else:
            res = 'WHERE ' +  logic_str.format(comparison=comparison,between=between,inlist=inlist,likepattern=likepattern,isnull=isnull)
        return res
    # -------------------------------------------------------------------------------------------
    def get_insert_query(self,table_name:str,items:dict)->str:
        '''INSERT INTO 테이블명 (키1, 키2, ...) VALUES (값1, 값2, ...);'''
        return f'''INSERT INTO "{table_name}" ({",".join(map(self._get_stred_item,items.keys()))}) VALUES ({",".join(map(self._get_stred_item,items.values()))});'''
    # --------------------------
    def get_select_query(self,table_name:str,items:list=[],where_option:dict={},sort_option:tuple={'id','오름차순'}):
        '''SELECT col1, col2 ... FROM 테이블명 WHERE 조건 ORDER BY col ASC/DESC'''
        where_str = self._get_where_str(**where_option) if where_option else ''
        sort_str = f'''ORDER BY {sort_option[0]} {"DESC" if sort_option[1] == "내림차순" else "ASC"}'''
        return f'''SELECT {",".join(map(self._get_stred_item,items)) if items else "*"} FROM "{table_name}" {where_str} {sort_str};'''
    # --------------------------
    def get_update_query(self,table_name:str,items:dict,where_option:dict={}):
        '''UPDATE 테이블명 SET 키1 = 값1, 키2 = 값2 ... WHERE 조건'''
        where_str = self._get_where_str(**where_option) if where_option else ''
        return f'''UPDATE "{table_name}" SET {','.join([f'''"{k}" = {self._get_stred_item(v)}''' for k,v in items.items()])} {where_str};'''
    # --------------------------
    def get_delete_query(self,table_name:str,where_option:dict={}):
        '''DELETE FROM 테이블명 WHERE 조건'''
        where_str = self._get_where_str(**where_option) if where_option else ''
        return f'''DELETE FROM "{table_name}" {where_str};'''

    def get_delete_query_by_item(self,table_name:str,items:dict):
        '''DELETE FROM 테이블명 WHERE 조건 - 모두 일치하는 항목 삭제'''
        sub_where_str = 'WHERE ' + " AND ".join([f'''"{k}" = "{v}"''' for k,v in items.items()])
        where_str = f'''WHERE id = (SELECT MAX(id) FROM {table_name} {sub_where_str})''' # 중복이 있으면 id가 가장 큰 것을 삭제
        return f'''DELETE FROM "{table_name}" {where_str};'''

# ===========================================================================================
if __name__ == '__main__':
    qb = QueryBuilder()
    res = qb.get_insert_query('users',{'name':'Tom','age':23,'city':'Seoul'})
    print(res)
    res = qb._get_where_str(comparison=[('col1','<',13),('col2','=',13)],between=[('col3',13,39),('col4',1,300)],inlist=[('col5',[1,2,3,43])],likepattern=[('col6','%afse%')],isnull=[('col7',True),('col8',False)], \
                            logic_str='{comparison[0]} AND {comparison[1]} OR {between[0]} AND NOT {between[1]} AND {inlist[0]} OR {likepattern[0]} AND {isnull[0]} AND {isnull[1]}')
    print(res)
    res = qb.get_select_query('users',['name','city'],{'comparison':[('age','>=',25)]})
    print(res)
    res = qb.get_update_query('users',{'name':'Tom','age':23},{'likepattern':[('city','S%')]})
    print(res)
    res = qb.get_delete_query('users',{'comparison':[('name','=','Tom')]})
    print(res)
