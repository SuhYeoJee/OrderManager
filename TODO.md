

# Order Manager

> bond 테이블 powder명 정규화함 (소문자, #->_)
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

## TODO
- [x] DB 뷰어
  - [x] 테이블에서 버튼 눌러서 세부정보 보기
    - [x]  View.update_table_data
  - [x] 이미지 처리
- [ ] 수주 관리
  - [x] 수주 입력
  - [ ] 완료 처리
    - [ ] shipping 입력폼. 
      - [ ] 이거 orders.name이 같은 항목 한 번에 보여줘야함. 
      - [ ] 값 수정은 shipping만, update연산
    - [ ] 이거 그냥 id 가져와서 날짜만 입력하게 하자


- [ ] 문서 인쇄
  - [ ] 수주 인쇄
    - [ ] 날짜 구간 선택
    - [ ] 미리보기
  - [ ] sp, ip 인쇄
    - [ ] 미리보기

- [ ] ~~재고 관리~~
- [ ] 단가 계산기 <- 별도 프로그램으로 분리
  - [ ] 본드
  - [ ] 세그멘트
  - [ ] 아이템

### 진행중 


#### 아 본드 입력기에 파우더가 없음
ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ

본드 입력기라는게
비율을 착착 쓰면
밀도를 자동으로 보여줘야함 
innerwidget

이거 본드 db도 정규화해서 powder_1, powder1_rate 하면 안되나 
그게 낫겠는데요 

#### 계산기
- 가격테이블 
날짜, 아이템명, 가격
이거 pk 하지 말자




#### nONE 선택 
이거 그냥 코드에서 '', 0값이나 2000-1-1이면 예외처리 해야겠는데


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
5. 매핑함수 작성(ctrl)
`on_json_request(self,json_reqeust)`
6. 시그널 매핑(ctrl) 
`self.view.json_request.connect(self.on_json_request)`