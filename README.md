## 😡 Project Architecture
<br>
<p align="center">
  <img src="https://github.com/user-attachments/assets/3fa480c4-7570-415d-92b9-6530504efd16" width="80%">
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


