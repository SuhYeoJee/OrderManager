if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
from dataclasses import dataclass, asdict
from typing import Optional, Union, Literal, List, Dict, Tuple
from src.imports.pyqt5_imports import *
from refactoring.db.DBManager import DBManager


@dataclass
class IPDocItemParam:
    item:str
    amount:int
    # code:str # 안쓰는거같음 리팩토링 완료후 확인좀 
    def to_dict(self): return asdict(self)

@dataclass
class IPDocParam:
    dbm: DBManager

    group: str = ''
    engrave: str = ''
    customer: str = ''
    description: str = ''
    due_date: Optional[QDate] = None
    order_date: Optional[QDate] = None

    item1: IPDocItemParam
    item2: Optional[IPDocItemParam] = None
    item3: Optional[IPDocItemParam] = None
    item4: Optional[IPDocItemParam] = None

    def to_dict(self): 
        return {k:v for k,v in asdict(self).items() if k != 'dbm'}

@dataclass
class SPDocParam:
    dbm: DBManager

    name: str = ''
    workload: int = 0

    def to_dict(self): 
        return {k:v for k,v in asdict(self).items() if k != 'dbm'}
