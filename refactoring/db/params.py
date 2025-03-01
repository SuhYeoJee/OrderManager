from dataclasses import dataclass, asdict
from typing import Optional, Union, Literal, List, Dict, Tuple
from src.imports.pyqt5_imports import *


@dataclass
class InsertParams:
    table_name :str
    column_value_pairs: Dict[str, Union[str, int, float,QDate,QDateTime]]
    # -------------------------------------------------------------------------------------------
    def to_dict(self): return asdict(self)
# ===========================================================================================
# where: SqliteQueryBuilder._build_where_clause 참조
@dataclass
class SelectParams:
    table_name :str
    columns: Optional[List[str]] = None
    where: Optional[Dict[str, List[Tuple]]] = None  # ex// {'comparison':[('column_name','=',value),]}
    sort: Optional[Tuple[str, Literal['ASC','asc','DESC','desc']]] = None  # ex// ('name', 'ASC')
    # -------------------------------------------------------------------------------------------
    def to_dict(self): return asdict(self)
# ===========================================================================================
@dataclass
class UpdateParams:
    table_name :str
    column_value_pairs: Dict[str, Union[str, int, float,QDate,QDateTime]]
    where: Optional[Dict[str, List[Tuple]]] = None  # ex// {'comparison':[('column_name','=',value),]}
    # -------------------------------------------------------------------------------------------
    def to_dict(self): return asdict(self)
# ===========================================================================================
@dataclass
class DeleteParams:
    table_name :str
    column_value_pairs: Optional[Dict[str, Union[str, int, float,QDate,QDateTime]]] = None
    where: Optional[Dict[str, List[Tuple]]] = None  # ex// {'comparison':[('column_name','=',value),]}
    # -------------------------------------------------------------------------------------------
    def __post_init__(self):
            # column_value_pairs와 where 둘 중 하나만
            if self.column_value_pairs and self.where:
                raise ValueError("Either 'column_value_pairs' or 'where' should be provided, not both.")
            if not self.column_value_pairs and not self.where:
                raise ValueError("At least one of 'column_value_pairs' or 'where' must be provided.")
    def to_dict(self): return asdict(self)
# ===========================================================================================
if __name__=="__main__":
    print(asdict(InsertParams('as',{'s',1})))
