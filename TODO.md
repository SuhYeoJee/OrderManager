

# Order Manager

> bond 테이블 powder명 정규화함 (소문자, #->_)
> 테이블 cols 반드시 소문자요구 (다이얼로그 자동화)

## TODO
- [ ] DB 뷰어
- [ ] 문서 생성
- [ ] None값, ''값 처리

### 진행중 

#### DB 뷰어
DB 셀렉트 & TABLE 뷰를 만들자. 
- [ ] 테이블 다이얼로그 제작
    - [ ] sp
    - [ ] ip
- [ ] select 결과에서 다이얼로그로 바로 여는 버튼 추가

#### 문서 자동생성
딸깍으로 문서를 자동 생성하고싶다. 
어떻게 하지

필요한 input을 넣으면 json파일을 생성하고 path를 반환하는 함수 작성. 
모델에 작성

##### sp

아 레거시코드 도움이 안되네



## 나중에

- `DB_PATH='./config/NOVA.db'` 가 model, dialog에 각각 하드코딩 되어있음. 나중에 환경변수로 빼던가 
- check 사용하게되면 리스트반환 함수 필요함(테스트코드)




## 유지보수

### 다이얼로그 등록하는 방법
1. ~~(자동화됨) Dialog.py에 다이얼로그 객체 생성~~
2. ~~(자동화됨) View.dialog_infos에 {"테이블명":클래스} 쌍 추가~~
3. ~~(자동화됨) Controller.init_signals에 추가 ~~

- ui 폴더에 {table_name}Dialog.ui 확인
- db에 table_name 테이블 확인
- Dialog.py에 DB_PATH 확인

