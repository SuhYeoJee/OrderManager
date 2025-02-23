

# Order Manager

> bond 테이블 powder명 정규화함 (소문자, #->_)
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

## TODO
- [ ] DB 뷰어
  - [ ] 테이블에서 버튼 눌러서 세부정보 보기
    - [ ]  View.update_table_data
  - [x] 이미지 처리
- [ ] 수주 관리
  - [x] 수주 입력
  - [ ] 완료 처리
    - [ ] shipping 입력폼. 
      - [ ] 이거 orders.name이 같은 항목 한 번에 보여줘야함. 
      - [ ] 값 수정은 shipping만, update연산
- [ ] ~~재고 관리~~

### 진행중 
  - [ ] 테이블에서 버튼 눌러서 세부정보 보기
    - [ ]  View.update_table_data

> if 단독 조회가 가능한 col인 경우:
근데 저이가 이걸 어떻게 아나요. 
... 다이얼로그 view에 key가 있는지 확인하면 된다...!!
이거 col 명을 table명이랑 맞춰야하는데
seg1,seg2 이런거 안맞음 언더바? 
  1. 언더바 기준으로 테이블명_나머지정보 `segment_1`
아 이거 바꾸려면 너무 많은 걸 바꿔야하는데 
ui 위젯명 다바꿔야함

분명 더 좋은 다른 방법이 있을것임
근데 사실 통일하는게 편한거 같기도 함
디비에서 REFERENCES로 찾고 바꾸기. 
하지만 또다른 문제가 있다면 
이 값을 어느 col에서 찾아야하는가가 있다. 
segment 제외하면 다 name임 
그럼 차라리 세그먼트도 네임으로 바꾸지 
name -> fullname, code -> name

많은 일이 필요함.. 
일단 세그먼트 다 바꿈
이거 다 바꾸고 연산 고장나는곳 없는지 최종확인하자


## 나중에
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