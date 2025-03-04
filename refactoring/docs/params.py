from dataclasses import dataclass, asdict
from typing import Optional, Union, Literal, List, Dict, Tuple
from src.imports.pyqt5_imports import *
from refactoring.db import DBManager


@dataclass
class IPDocItemParam:
    name:str
    amount:int
    # code:str # 안쓰는거같음 리팩토링 완료후 확인좀 
    def to_dict(self): return asdict(self)

@dataclass
class IPDocParam:
    item1: IPDocItemParam
    item2: Optional[IPDocItemParam] = None
    item3: Optional[IPDocItemParam] = None
    item4: Optional[IPDocItemParam] = None

    group: str = ''
    engrave: str = ''
    customer: str = ''
    description: str = ''
    due_date: Optional[QDate] = None
    order_date: Optional[QDate] = None

    def to_dict(self): return asdict(self)

@dataclass
class SPDocParam:
    name: str = ''
    workload: int = 0

    def to_dict(self): return asdict(self)
