틱톡 모바일 작업용 PWA v1

핵심:
- 스마트폰 브라우저에서 접속해서 쓰는 웹앱 방식입니다.
- 틱톡 링크를 넣으면 서버/PC에서 영상을 받고, 작업 폴더를 만듭니다.
- 저장 폴더는 날짜+시간+작업번호로 구분됩니다.
- PC와 같은 네트워크에 있는 스마트폰에서 먼저 테스트하는 구조입니다.

저장 구조:
app/data/jobs/
  20260524_143012_tiktok/
    video/
      source.mp4
    frames/
      frame1.jpg
      frame2.jpg
      frame3.jpg
      frame4.jpg
      frame5.jpg
      frame6.jpg
    links/
      source_tiktok.txt
      coupang.txt
      coupas.txt
    notes/
      memo.txt

실행 순서:
1. 압축 풀기
2. 폴더 안에서 cmd 열기
3. pip install -r requirements.txt
4. python app.py
5. PC 브라우저에서 http://127.0.0.1:5000 접속
6. 스마트폰에서는 같은 와이파이에서 PC IP로 접속
   예: http://192.168.0.10:5000

스마트폰 홈화면 추가:
- 안드로이드 크롬: 메뉴 → 홈 화면에 추가
- 아이폰 사파리: 공유 버튼 → 홈 화면에 추가

주의:
- 밖에서도 쓰려면 이 앱을 Render, Railway, VPS 같은 서버에 올려야 합니다.
- 구글 렌즈는 자동 업로드가 아니라 버튼으로 열고, 프레임 이미지를 직접 공유/검색하는 방식이 안정적입니다.
- 쿠파스 API 연동은 다음 버전에서 붙이는 것을 추천합니다. 이 v1은 모바일 화면/저장 구조 테스트용입니다.
