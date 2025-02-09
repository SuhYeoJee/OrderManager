..... 어쩌지


# 일단 DB 관리자를 만들자. 
- [ ] DB 뷰어
- [ ] test코드 // 외래키, check 조건 추가, 리스트반환 동작 확인하기
    - [x] 사용 가능한 vals 반환하기
    - [x] 외래키목록 가져오기 
    - [ ] 콤보박스에 리스트 등록


##### DB 뷰어
DB 셀렉트 & TABLE 뷰를 만들자. 

DB 뷰어가 COL이름을 제대로 읽으려면 쿼리를 2번 보내야하는데 그거 처리 RUN 함수에서 호출 2번 하고 묶는걸로 수정

ㄴ 이게 대체 무슨 소리야

- [ ] 테이블 다이얼로그 제작
    - [x] (연결완료)customer
    - [x] powder
    - [x] shank
    - [x] submaterial (=diamond)
    - [x] diamond
    - [ ] bond - 진행중
    - [ ] segment
    - [ ] item
    - [ ] orders
    - [ ] sp
    - [ ] ip

- [ ] select 결과에서 다이얼로그로 바로 여는 버튼 추가

## 유지보수

### 다이얼로그 등록하는 방법
1. Dialog.py에 다이얼로그 객체 생성
    - clear, set_fks, get_inputs, set_datas 정의
2. ~~(자동화됨) View.dialog_infos에 {"테이블명":클래스} 쌍 추가~~
3. ~~(자동화됨) Controller.init_signals에 추가 ~~
- ui 폴더에 {table_name}Dialog.ui 있어야함
- db에 table_name 테이블 있어야함


다이얼로그 객체 생성할 때 
cols 자동으로 가져오는 방법 없나 
model이 넘겨주면 되긴 할텐데 
다이얼로그를 모델에 꽂을라면.. 
좀 빡세긴함..
pre 가져올때 달라고하면 되나
pre리스폰스에 cols추가하기 

내가해냄