from dataclasses import dataclass, asdict
from typing import Optional, Union, Literal, List, Dict, Tuple
from src.imports.pyqt5_imports import *

@dataclass
class WhereParam:
    comparison: Optional[List[Tuple[
        str, # column_name
        Literal['>','<','=','!=','>=','<='], # operator
        Union[str, int, float, QDate, QDateTime] # operand
    ]]] = None

    between: Optional[List[Tuple[
        str, # column_name
        Union[str, int, float, QDate, QDateTime], # start
        Union[str, int, float, QDate, QDateTime]  # end
    ]]] = None

    inlist: Optional[List[Tuple[
        str, # column_name
        List[Union[str, int, float, QDate, QDateTime]]
    ]]] = None

    like: Optional[List[Tuple[
        str, # column_name
        str # pattern
    ]]] = None

    isnull: Optional[List[Tuple[
        str, # column_name
        bool # is_null 
    ]]] = None

    logic: str = None

    def to_dict(self): return asdict(self)
    def get_conditions(self):
        conditions = {k: v for k, v in asdict(self).items() if v is not None}
        conditions.pop('logic',None)
        return conditions

@dataclass
class SortParam:
    column_name: str = 'id'
    is_desc: bool = True

@dataclass
class InsertParam:
    table_name :str
    column_value_pairs: Dict[str, Union[str, int, float,QDate,QDateTime]]

    def to_dict(self): return asdict(self)

    def get_filtered_column_value_pairs(self):
        return {k: v for k, v in self.column_value_pairs.items() if v is not None}

@dataclass
class SelectParam:
    table_name :str
    columns: Optional[List[str]] = None
    where: Optional[WhereParam] = None
    sort: Optional[SortParam] = None
    limit: Optional[int] = None

    def to_dict(self): 
        return asdict(self)

@dataclass
class UpdateParam:
    table_name :str
    column_value_pairs: Dict[str, Union[str, int, float,QDate,QDateTime]]
    where: Optional[WhereParam] = None

    def to_dict(self): return asdict(self)

    def get_filtered_column_value_pairs(self):
        return {k: v for k, v in self.column_value_pairs.items() if v is not None}

@dataclass
class DeleteParam:
    table_name :str
    column_value_pairs: Optional[Dict[str, Union[str, int, float,QDate,QDateTime]]] = None
    where: Optional[WhereParam] = None

    def __post_init__(self):
            # column_value_pairs와 where 둘 중 하나만
            if self.column_value_pairs and self.where:
                raise ValueError("Either 'column_value_pairs' or 'where' should be provided, not both.")
            if not self.column_value_pairs and not self.where:
                raise ValueError("At least one of 'column_value_pairs' or 'where' must be provided.")
            
    def to_dict(self): return asdict(self)

    def get_filtered_column_value_pairs(self):
        return {k: v for k, v in self.column_value_pairs.items() if v is not None}


# ===========================================================================================
if __name__=="__main__":
    w = WhereParam(comparison=[('as','>',2)])
    p = asdict(DeleteParam('as',where=w))
    print(isinstance(p['where'],dict))
