
import re

class QueryBuilder():
    def __init__(self):...
    # --------------------------
    def _get_where_str(self,logic_str:str='',**kwargs):
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
            [(컬럼,True(값 부재)),(컬럼,False(값 존재))]

        조건식 논리를 스트링으로 입력 (기본: AND 연결)
        논리: AND, OR, NOT
        logic_str = '{comparison[0]} AND {comparison[1]} OR NOT {between[0]}'
        '''
        bindings = {'comparison':[],'between':[],'inlist':[],'likepattern':[]}
        comparison = []
        if 'comparison' in kwargs.keys():
            for i in kwargs['comparison']:
                col,op,val = i
                comparison.append(f'''"{col}" {op} ?''')
                bindings['comparison'].append(val)

        between = []
        if 'between' in kwargs.keys():
            for i in kwargs['between']:
                col,start,end = i
                between.append(f'''"{col}" BETWEEN ? AND ?''')
                bindings['between'].append([start,end])

        inlist = []
        if 'inlist' in kwargs.keys():
            for i in kwargs['inlist']:
                col,vals = i
                inlist.append(f'''"{col}" IN ({','.join(['?']*len(vals))})''')
                bindings['inlist'].append(vals)

        likepattern = [] 
        if 'likepattern' in kwargs.keys():
            for i in kwargs['likepattern']:
                col,pattern = i
                likepattern.append(f'''"{col}" LIKE ?''')
                bindings['likepattern'].append(pattern)
        
        isnull = []
        if 'isnull' in kwargs.keys():
            for i in kwargs['isnull']:
                col,flag = i
                isnull.append(f'''"{col}" IS {'' if flag else 'NOT'} NULL''')
        # -------------------------------------------------------------------------------------------
        def extract_and_get_binding_values(logic_str, bindings):
            keys = re.findall(r'\{(.*?)\}', logic_str)
            result = []
            for key in keys:
                key_parts = key.split('[')
                base_key = key_parts[0]
                index = int(key_parts[1].rstrip(']'))
                if base_key in ['isnull']:continue
                elif base_key in ['between','inlist']:
                    result.extend(bindings[base_key][index])
                else:
                    result.append(bindings[base_key][index])
            return result
        # -------------------------------------------------------------------------------------------
        if not logic_str:
            res = 'WHERE ' + ' AND '.join (comparison+between+inlist+likepattern+isnull)
            res_bindings = []
            res_bindings.extend(bindings['comparison'])
            res_bindings.extend([y for x in bindings['between'] for y in x])
            res_bindings.extend([y for x in bindings['inlist'] for y in x])
            res_bindings.extend(bindings['likepattern'])
        else:
            res = 'WHERE ' +  logic_str.format(comparison=comparison,between=between,inlist=inlist,likepattern=likepattern,isnull=isnull)
            res_bindings = extract_and_get_binding_values(logic_str,bindings)
        return res, res_bindings
    # -------------------------------------------------------------------------------------------
    def get_insert_query(self,table_name:str,items:dict):
        '''INSERT INTO 테이블명 (키1, 키2, ...) VALUES (?,?,...);, (값1,값2,...)'''
        bindings = list(items.values())
        return f'''INSERT INTO "{table_name}" ({",".join([f'"{x}"' for x in items.keys()])}) VALUES ({",".join(['?']*len(bindings))});''',bindings
    # --------------------------
    def get_select_query(self,table_name:str,items:list=[],where_option:dict={},sort_option:tuple=('id','오름차순')):
        '''SELECT col1, col2 ... FROM 테이블명 WHERE 조건 ORDER BY col ASC/DESC;,bindings'''
        where_str,bindings = self._get_where_str(**where_option) if where_option else ('',[])
        sort_str = f'''ORDER BY {sort_option[0]} {"DESC" if sort_option[1] == "내림차순" else "ASC"}'''
        return f'''SELECT {",".join([f'"{x}"' for x in items]) if items else "*"} FROM "{table_name}" {where_str} {sort_str};''',bindings
    # --------------------------
    def get_update_query(self,table_name:str,items:dict,where_option:dict={}):
        '''UPDATE 테이블명 SET 키1 = 값1, 키2 = 값2 ... WHERE 조건;,bindings'''
        where_str,where_bindings = self._get_where_str(**where_option) if where_option else ('',[])
        bindings = list(items.values()) + where_bindings
        return f'''UPDATE "{table_name}" SET {','.join([f'''"{k}" = ?''' for k in items.keys()])} {where_str};''',bindings
    # --------------------------
    def get_delete_query(self,table_name:str,where_option:dict={}):
        '''DELETE FROM 테이블명 WHERE 조건'''
        where_str,bindings = self._get_where_str(**where_option) if where_option else ('',[])
        return f'''DELETE FROM "{table_name}" {where_str};''',bindings
    # --------------------------
    def get_delete_query_by_item(self,table_name:str,items:dict):
        '''DELETE FROM 테이블명 WHERE 조건 - 모두 일치하는 항목 삭제'''
        sub_where_str = 'WHERE ' + " AND ".join([f'''"{k}" = ?''' for k in items.keys()])
        bindings = list(items.values())
        where_str = f'''WHERE id = (SELECT MAX(id) FROM {table_name} {sub_where_str})''' # 중복이 있으면 id가 가장 큰 것을 삭제
        return f'''DELETE FROM "{table_name}" {where_str};''',bindings

# ===========================================================================================
if __name__ == '__main__':
    qb = QueryBuilder()
    # res = qb._get_where_str(comparison=[('col1','<',13),('col2','=',13)],between=[('col3',13,39),('col4',1,300)],inlist=[('col5',[1,2,3,43])],likepattern=[('col6','%afse%')],isnull=[('col7',True),('col8',False)], \
    #                         logic_str='{comparison[0]} AND {comparison[1]} OR {between[0]} AND NOT {between[1]} AND {inlist[0]} OR {likepattern[0]} AND {isnull[0]} AND {isnull[1]}')
    # print(res)
    res = qb.get_insert_query('users',{'name':'Tom','age':23,'city':'Seoul'})
    print(res)
    res = qb.get_select_query('users',['name','city'],{'comparison':[('age','>=',25)]})
    print(res)
    # res = qb.get_update_query('users',{'name':'Tom','age':23},{'likepattern':[('city','S%')]})
    # print(res)
    # res = qb.get_delete_query('users',{'comparison':[('name','=','Tom')]})
    # print(res)
    # res = qb.get_delete_query_by_item('users',{'name':'Tom','city':'busan','age':24})
    # print(res)

