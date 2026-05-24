Threads Coupas Tool v4

기능:
- 틱톡 다운로드 사이트 열기: https://tikvideo.app/ko
- 구글 렌즈 열기
- 쿠팡 상품 링크를 쿠파스 링크로 변환
- API 키 저장/지우기
- 쿠파스 링크 복사
- 내 GPTs 열기
- 메모 저장

Render 설정:
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app --bind 0.0.0.0:$PORT

업로드 파일:
app.py
requirements.txt
README_KR.txt
templates/
static/
