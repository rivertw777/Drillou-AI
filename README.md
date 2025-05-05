## 😡 Project Architecture
<br>
<p align="center">
  <img src="https://github.com/user-attachments/assets/280732e8-cec3-401c-b87e-e5f145097f9c" width="80%">
</p>
<br>

### 패키지 설치
pip install -r requirements.txt

### FastAPI 실행
uvicorn app.main:app --reload

### 스웨거 
http://127.0.0.1:8000/docs

### Celery 실행
celery -A app.celery_app worker -l info -P eventlet

### Flower 실행
celery -A app.celery_app flower


