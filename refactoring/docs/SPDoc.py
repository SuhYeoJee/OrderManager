if __debug__:
    import sys
    sys.path.append(r"X:\Github\OrderManager")
# ===========================================================================================
from src.imports.config import DATE_FORMAT, DATE_KO_FORMAT
from src.imports.pyqt5_imports import QDate

from refactoring.db import DBManager,InsertParam,SelectParam,SortParam
from refactoring.docs.JsonManager import JsonManager
from refactoring.docs.params import SPDocParam
from refactoring.utils.SafeList import SafeList
from math import ceil

class SPDoc(JsonManager):
    def __init__(self,dbm:DBManager,p:SPDocParam):
        self.dbm =dbm
        self.p = p
        self.name = self._get_new_sp_name()
        self.file_path = f'./test/{self.name}.json'
        # self.file_path = f'./doc/sp/{self.name}.json'
        super().__init__(self.file_path)

        self.build_sp()

    @JsonManager.auto_save
    def build_sp(self):
        self.data['inputs'] = self.p.to_dict()
        self.data['loads'] = self._load_segment_and_bond()
        self.data['autos'] = self._build_autos()
    # -------------------------------------------------------------------------------------------
    def _get_new_sp_name(self):
        last_sp_year,last_sp_no = self._get_last_sp_year_and_no_from_db()
        now_year =str(QDate.currentDate().year())
        if last_sp_year == now_year:
            new_sp_name = f"{last_sp_year}-SP{int(last_sp_no[2:])+1:04}"
        else:
            new_sp_name = f"{now_year}-SP{1:04}"
        # recent_sp_name = ''
        # new_sp_name = f"{new_sp_name}-{recent_sp_name}" # 이거 진짜 최선인지 물어보기
        return new_sp_name
    # -------------------------------------------------------------------------------------------
    def _get_last_sp_year_and_no_from_db(self):
        try:
            [last_sp_name] = self.dbm.select_records(SelectParam('sp',['name'],sort=SortParam(),limit=1))
            last_sp_year,last_sp_no = last_sp_name[1].split('-')
        except ValueError:
            last_sp_year,last_sp_no = "2000","SP0000"
        return last_sp_year,last_sp_no
    
    def _load_segment_and_bond(self):
        self.segment = SafeList(self.dbm.select_records_by_comparison('segment','name',self.p.name)).safe_get(0)
        self.bond = SafeList(self.dbm.select_records_by_comparison('bond','name',self.segment.get('bond'))).safe_get(0)
        return {'segment':self.segment,'bond':self.bond}

    def _build_autos(self)->dict:
        autos = self._build_default_autos()
        autos['name'] = self.name # recent-sp가 필요하다면 여기서 self.data['loads']로 붙일 수 있음
        autos['creation_date'] = QDate.currentDate().toString(DATE_KO_FORMAT)
        autos['segment_config'] = self._build_segment_config()
        autos['segment_density'] = self._build_segment_density()
        autos['workload'] = self._build_workload()
        autos['verification'] = self._build_verification()
        autos['powder_config'] = self._build_powder_config()
        
        return autos
    # -------------------------------------------------------------------------------------------

    def _build_default_autos(self)->dict:
        autos = {}
        autos['segment_weight'] = self._build_segment_weight()
        autos['concent'] = self._build_concent()
        return autos

    def _build_concent(self)->float:
        return float(self.segment.get('concent',0))/4.4*100

    def _build_segment_weight(self)->float:
        segment_volume = float(self.segment.get('v',0))
        bond_density = float(self.bond.get('density',0))
        segment_rel_density = float(self.segment.get('rel_density',0))
        loss = float(self.segment.get('loss',0))

        segment_weight = segment_volume * bond_density * segment_rel_density * loss
        return segment_weight
    
    def _build_segment_config(self)->dict:
        segment_weight = float(self.data['autos']['segment_weight'])
        segment_volume = float(self.segment.get('v',1)) #avoid zero division
        segment_concent = float(self.segment.get('concent',0))

        diamond_weight = segment_volume * segment_concent * 0.2
        diamond_volume = diamond_weight /3.51
        diamond_volume_rate = diamond_volume / segment_volume

        bond_volume = segment_volume - diamond_volume
        bond_volume_rate = bond_volume / segment_volume
        bond_weight = bond_volume_rate * segment_weight

        total_volume =  diamond_volume + bond_volume
        total_volume_Rate = diamond_volume_rate + bond_volume_rate
        total_weight = diamond_weight + bond_weight

        return {
            'diamond_weight':diamond_weight, 'diamond_volume':diamond_volume, 'diamond_volume_rate':diamond_volume_rate,
            'bond_weight':bond_weight, 'bond_volume':bond_volume, 'bond_volume_rate':bond_volume_rate, 
            'total_weight':total_weight, 'total_volume':total_volume, 'total_volume_Rate':total_volume_Rate
        }

    def _build_segment_density(self)->dict:
        bond_density = float(self.bond.get('density',0))
        bond_volume_rate = float(self.data['autos']['bond_volume_rate'])
        diamond_volume_rate = float(self.data['autos']['diamond_volume_rate'])
        total_weight = float(self.data['autos']['total_weight'])
        segment_volume = float(self.segment.get('v',1)) #avoid zero division
        segment_concent = float(self.segment.get('concent',0))

        theo_density1 = bond_density * bond_volume_rate + diamond_volume_rate * 3.51
        theo_density2 = bond_density * bond_volume_rate + segment_concent * 0.2
        final_density = total_weight / segment_volume
        final_rel_density = final_density / theo_density1
        benchmark_density = theo_density1 * 0.94

        return {'theo_density1':theo_density1,'theo_density2':theo_density2,
                'final_density':final_density,'final_rel_density':final_rel_density,
                'benchmark_density':benchmark_density}

    def _build_workload(self)->dict:
        workload = self.p.workload
        total_weight = float(self.data['autos']['total_weight'])
        diamond_weight = float(self.data['autos']['diamond_weight'])
        diamond1_rate = float(self.segment.get('diamond1_rate',0))
        diamond2_rate = float(self.segment.get('diamond2_rate',0))
        diamond3_rate = float(self.segment.get('diamond3_rate',0))

        bondmix_weight = total_weight - diamond_weight

        min_bondmix_workload = workload * (bondmix_weight)
        bond_workload = ((min_bondmix_workload + 4999) // 5000) * 5000

        segment_work = bond_workload // bondmix_weight if bondmix_weight else 0
        bondmix_workload = segment_work * bondmix_weight

        diamond1_weight = ceil(diamond_weight * segment_work * diamond1_rate/10)
        diamond2_weight = ceil(diamond_weight * segment_work * diamond2_rate/10)
        diamond3_weight = ceil(diamond_weight * segment_work * diamond3_rate/10)

        return {'bond_workload':bond_workload,'segment_work':segment_work,'bondmix_workload':bondmix_workload,
                'diamond1_weight':diamond1_weight,'diamond2_weight':diamond2_weight,'diamond3_weight':diamond3_weight}

    def _build_verification(self)->dict:
        bondmix_workload = float(self.data['autos']['bondmix_workload'])
        diamond1_weight = float(self.data['autos']['diamond1_weight'])
        diamond2_weight = float(self.data['autos']['diamond2_weight'])
        diamond3_weight = float(self.data['autos']['diamond3_weight'])
        total_weight = float(self.data['autos']['total_weight'])
        segment_work = int(self.data['autos']['segment_work'])

        verification_weight = bondmix_workload + diamond1_weight + diamond2_weight + diamond3_weight
        verification_count = total_weight * segment_work
        return {'verification_weight':verification_weight,'verification_count':verification_count}

    def _build_powder_config(self)->dict:
        powder_config = {}
        for idx in range(1,7):
            powder_config.update(self._build_powder_weight(idx))

        powder_config['total_rate'] = sum(val for key,val in self.powder.items() \
                                          if key.endswith("_rate") and '6' not in key) #powder 6: p2o5 예외
        powder_config['total_weight'] = sum(val for key,val in self.powder.items() \
                                            if key.endswith("_weight") and '6' not in key)

        return powder_config

    def _build_powder_weight(self,idx):
        powder = {}
        bond_workload = self.data['autos'].get(bond_workload,0)
        powder_rate = self.bond.get(f'powder{idx}_rate',0)
        powder_weight = (powder_rate/100)*bond_workload
        
        powder[f'powder{idx}_name'] = self.bond[f'powder{idx}_name']
        powder[f'powder{idx}_rate'] = powder_rate
        powder[f'powder{idx}_weight'] = powder_weight 
        return powder

# ===========================================================================================