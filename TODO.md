

# Order Manager

> bond 테이블 powder명 정규화함 (소문자, #->_)
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

## TODO
- [ ] DB 뷰어
- [ ] 수주 관리
- [ ] 재고 관리

### 진행중 

#### DB 뷰어
DB 셀렉트 & TABLE 뷰를 만들자. 
- [ ] 테이블 다이얼로그 제작
    - [ ] sp
    - [ ] ip


##### sp
다이얼로그 대강 구현함

- 다이얼로그
- [ ] 스핀박스
    - [ ] 값범위
- [ ] 글꼴
- [ ] 테두리
- [ ] 이미지 뷰
- [ ] 다이얼로그에 위젯 연결

- [ ] 계산창 새로 만들어야한다
> 차라리 sp뷰를 별도 모달로 띄우고 계산창은 기존 모달에 표시하죠

오더장 만들고 ip, sp자동생성 연결로직부터 만들면 될듯함

- 위젯 채우는 함수 작성
1. 값 load 할 때 path넘기면서 파일 내용도 넘겨야할듯
2. 넘어온 내용 표시하는건 wfa.py 테스트코드

#### sp 보기
sp 다이얼로그에 버튼을 하나 만들어서 sp위젯 열기 매핑
매핑을 어디에? 뷰초기화. 
inst,upd,del에도 넣을지는 고민.


##### ip
-생성완-
위젯에 표시 필



#### 수주/재고 관리
이제 버튼을 하나 만들어서 누르면 다이얼로그를 꺼내와. 
버튼에 ui 연결좀. 
어캐하더라

아마따 이거 동적ui 짜야하네

다이얼로그를 띄웠는데
로드가 안됨. 


##### order
```
입력창
1탭
수주일자: 2025-02-17
수주번호: 자동생성 (2025-0001)
고객코드: customer(code)

2탭
제품그룹: 3"4Y40
각인: text

3탭
일련번호: 자동생성 (001)
제품명세: CW
주문수량: 30

일련번호: 자동생성 (002)
제품명세: CCW
주문수량: 30

2탭
제품그룹: DBS OR 60
각인: text

3탭
일련번호: 자동생성 (003)
제품명세:  T
주문수량: 5

+
```

이거 2탭 고르면 3탭 4칸 자동생성해서 콤보나 라벨로 박고
스핀박스로 수량지정
2탭에 선택. 버튼 만들어서 눌러야 3탭 생성. 





***


#### 테스트값 입력
- 세그먼트 본드 없는거 몇개 제외됨
- 세그먼트 다이아 이름 일치 안해서 제외함
- 아이템 세그먼트, 샹크, 서브 없는거 제외함


## 나중에
- check 사용하게되면 리스트반환 함수 필요함(테스트코드)
- 검색 안하고 sort만 하는 기능 쓰기 



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