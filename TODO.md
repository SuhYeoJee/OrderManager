

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
  - [ ] 수주 입력 동적 다이얼로그
    - [x] 다이얼로그 생성
    - [ ] 기능 연결
  - [ ] 수주 입력시 문서 자동생성
    - [ ] 문서 자동 생성
    - [ ] DB 업데이트
      - [ ] 각종 항목.. 
- [ ] 재고 관리
  - [ ] 재고 계산 로직 추가

### 진행중 

##### sp
- 위젯 수정
  - sp_dialog get_inputs에서 계산창 제외하기
    - 위젯명 접두어

sp 파우더 정규

- [ ] 이미지 뷰



##### 수주 동적 다이얼로그

일단 동적으로 증가하긴 함. 
일단 값이 읽어지긴 함. 

그럼 item_groupComboBox에 리스트 세팅해줘야함 
근데 사실 이게 pre리퀘 동작인데요
fk라고 치고 항목 추가한다음 숨길까
특징:  orders에는 원래 아이템이 들어간다 
아 근데 아이템 그룹은 프키가 아니다 
그리고 프키는 중복불가라 프키가 될수도 없다 
그니깐.. 아이템 값은 있음 
아이템 그룹이 없음 
그럼 로드를 할때 디비읽을 필요가 없네
전제는..
아이템 이름으로 아이템그룹/아이템타입을 분리가능
하다는게 전제.. 
그냥 띄.쓰. 기준으로 자르면 안될까 
어차피 일관성 없어서 내맘대로 해도 될듯
ㅋㅋㄹ

-> db에서 아이템네임/그룹/타입을 병합하는 안. 
그룹을 따로 쓰는 곳은 없긴함. 
이거 하면 sp ip 여러개 고쳐야함
하지만 더 편해진다는것은 변하지 않음


## 나중에
- check 사용하게되면 리스트반환 함수 필요함(테스트코드)
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