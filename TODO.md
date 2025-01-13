..... 어쩌지


# 일단 DB 관리자를 만들자. 
- [x] DB 명령어 생성 모듈
- [x] DB 인터페이스 모듈
- [ ] DB 뷰어
    - [ ] INSERT
    - [ ] UPDATE
    - [ ] DELETE
    - [ ] SELECT
- [ ] DB 설계
- [ ] DB 테스트값 입력


##### DB 뷰어
프로그램의 동작 5할이 DB를 구경하는 것이다. 
적절한 DB 뷰어가 필요함. 
일단 제일 단순하게는 TABLE에 값을 쭉 띄우는 형태겠지. 

DB 셀렉트 & TABLE 뷰를 만들자. 

DB 뷰어가 COL이름을 제대로 읽으려면 쿼리를 2번 보내야하는데 그거 처리 RUN 함수에서 호출 2번 하고 묶는걸로 수정
INSERT, UPDATE, DELETE, SELECT 구현
INSERT, UPDATE는 각각 ui를 공유하고 이는 테이블 별로 상이하다. 
delete는 단일  ui사용, 기존 항목 콤보박스로 표시 후 버튼으로 삭제. 