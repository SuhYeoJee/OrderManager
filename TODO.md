> bond 테이블 powder명 정규화함 (소문자, #->_)
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

`DB_PATH='./config/NOVA.db'` 가 model, dialog에 각각 하드코딩 되어있음. 나중에 환경변수로 빼던가 


# 일단 DB 관리자를 만들자. 
- [ ] DB 뷰어
- [ ] test코드 // 외래키, check 조건 추가, 리스트반환 동작 확인하기
    - [x] 사용 가능한 vals 반환하기
    - [x] 외래키목록 가져오기 
    - [ ] 콤보박스에 리스트 등록
- [ ] None값, ''값 처리

##### DB 뷰어
DB 셀렉트 & TABLE 뷰를 만들자. 
- [ ] 테이블 다이얼로그 제작
    - [x] (연결완료)customer
    - [x] (연결완료)powder
    - [x] (연결완료)shank
    - [x] (연결완료)submaterial (=diamond)
    - [x] (연결완료)diamond
    - [x] (연결완료)bond
    - [ ] segment
    - [ ] item
    - [ ] orders
    - [ ] sp
    - [ ] ip

- [ ] select 결과에서 다이얼로그로 바로 여는 버튼 추가



## 유지보수

### 다이얼로그 등록하는 방법
1. ~~(자동화됨) Dialog.py에 다이얼로그 객체 생성~~
2. ~~(자동화됨) View.dialog_infos에 {"테이블명":클래스} 쌍 추가~~
3. ~~(자동화됨) Controller.init_signals에 추가 ~~

- ui 폴더에 {table_name}Dialog.ui 있어야함
- db에 table_name 테이블 있어야함
- Dialog.py에 DB_PATH 확인

