..... 어쩌지


# 일단 DB 관리자를 만들자. 
- [x] DB 명령어 생성 모듈
- [x] DB 인터페이스 모듈
- [ ] DB 뷰어

- [ ] test코드 // 외래키, check 조건 추가, 리스트반환 동작 확인하기
- [ ] bindings 사용하는 쿼리로 변경 필
(_get_stred_item)를 value에 대해 안쓰는게 목적
    - [x] insert
    - [ ] select
    - [ ] update
    - [ ] delete
    - [x] where

##### DB 뷰어
DB 셀렉트 & TABLE 뷰를 만들자. 

DB 뷰어가 COL이름을 제대로 읽으려면 쿼리를 2번 보내야하는데 그거 처리 RUN 함수에서 호출 2번 하고 묶는걸로 수정

ㄴ 이게 대체 무슨 소리야

- [ ] 테이블 다이얼로그 제작
    - [ ] customer
    - [ ] powder
    - [ ] shank
    - [ ] submaterial
    - [ ] diamond
    - [ ] bond
    - [ ] segment
    - [ ] item
    - [ ] orders
    - [ ] sp
    - [ ] ip

- [ ] view에서 다이얼로그 초기화
- [ ] controller.init_signals에서 동작 매핑 
- [ ] select 결과에서 다이얼로그로 바로 여는 버튼 추가