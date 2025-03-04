

# Order Manager
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

`pyinstaller --onefile main.py`

## TODO

### 진행중 

#### 리팩토링

##### db colname변경
      # 일단 기존 방식이 너무 구림. 
      # col_name이 seg_amount, segment_처럼 되어있는데
      # 이걸 db명에서 찾아서 씀. 
      # 개선 반드시 필요함 
      # 개판난 이유가 뭐야
      # table에서 버튼자동생성하려고. 
      # 그럼 그걸 어떻게 수정하면 이름을 개판내지 않을 수 있어. 
      # 버튼 생성 대상에 _name을 일괄접미
      # 우오. 



## 유지보수

### 다이얼로그 등록하는 방법
1. ~~(자동화됨) Dialog.py에 다이얼로그 객체 생성~~
2. ~~(자동화됨) View.dialog_infos에 {"테이블명":클래스} 쌍 추가~~
3. ~~(자동화됨) Controller.init_signals에 추가 ~~

- ui 폴더에 {table_name}Dialog.ui 확인
- db에 table_name 테이블 확인
- Dialog.py에 DB_PATH 확인

### 시그널 추가하는 방법
1. 시그널 정의(view/dirlog/widget)
 `json_request = pyqtSignal(tuple)`
2. 발신 정의(view/dirlog/widget)
 `self.json_request.emit(('widget','sp', sp_path))`
3. 콜백함수 정의(view/dirlog/widget)
 `on_json_response(self,json_response)`
4. 모델함수 정의(model)
 `json_data(self,json_request)`
5. 매핑함수 작성(ctrl)
`on_json_request(self,json_reqeust)`
6. 시그널 매핑(ctrl) 
`self.view.json_request.connect(self.on_json_request)`