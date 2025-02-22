

# Order Manager

> bond 테이블 powder명 정규화함 (소문자, #->_)
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

## TODO
- [ ] DB 뷰어
  - [ ] sp
    - [x] sp 계산창 다이얼로그
    - [ ] sp 값채우기
  - [ ] ip
    - [ ] ip 값채우기
- [ ] 수주 관리
  - [x] 수주 입력 동적 다이얼로그
    - [x] 다이얼로그 생성
    - [x] 기능 연결
  - [X] 수주 입력시 문서 자동생성
    - [x] 문서 자동 생성
    - [X] DB 등록
  - [x] DB 업데이트
- [ ] 재고 관리
  - [ ] 재고 계산 로직 추가

### 진행중 

##### sp

sp 파우더 정규

- [ ] 이미지 뷰

baseui.set_datas_from_json_response 최적화필


##### 수주 동적 다이얼로그


여러 이슈가 있긴 하지만 일단 돌아감. 
SP이름문제: DB 업데이트 타이밍, 항목





## 나중에
- 검색 안하고 sort만 하는 기능 쓰기 

### 테스트값 입력
- 세그먼트 본드 없는거 몇개 제외됨
- 세그먼트 다이아 이름 일치 안해서 제외함
- 아이템 세그먼트, 샹크, 서브 없는거 제외함


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
5. 시그널 매핑(ctrl) 
`self.view.json_request.connect(self.on_json_request)`
6. 매핑함수 작성(ctrl)
`on_json_request(self,json_reqeust)`