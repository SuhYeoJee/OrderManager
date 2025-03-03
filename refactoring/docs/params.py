if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
from dataclasses import dataclass, asdict
from typing import Optional, Union, Literal, List, Dict, Tuple
from src.imports.pyqt5_imports import *
from refactoring.db.DBManager import DBManager

@dataclass
class IPDocParams:
    dbm: DBManager

    group: str = ''
    engrave: str = ''
    description: str = ''
    due_date: Optional[QDate]
    customer: str = ''
    order_date: Optional[QDate]

    item1: Dict[str,Union[str,int]] = {}
    item2: Dict[str,Union[str,int]] = {}
    item3: Dict[str,Union[str,int]] = {}
    item4: Dict[str,Union[str,int]] = {}

    def to_dict(self): 
        return {k:v for k,v in asdict(self).items() if k != 'dbm'}

@dataclass
class SPDocParams:
    dbm: DBManager

    name: str = ''
    workload: int = 0

    def to_dict(self): 
        return {k:v for k,v in asdict(self).items() if k != 'dbm'}
