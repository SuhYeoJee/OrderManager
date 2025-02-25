

# Order Manager
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

`pyinstaller --onefile main.py`

## TODO
- [ ] 문서 인쇄
  - [ ] 수주 인쇄

- [ ] ~~재고 관리~~
- [ ] ~~단가 계산기 <- 별도 프로그램으로 분리~~

### 진행중 

#### 인쇄

수주 인쇄폼..
애초에 sp2가 생기면서 수주보기가 무너진게 크다. 
이거 표 다시 보여주고 그거 캡쳐하면 됨

이거 너무 빡센데

#### 계산기
- 가격테이블 
날짜, 아이템명, 가격
이거 pk 하지 말자



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