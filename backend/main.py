import os
import sys
import hashlib

# Добавляем корневую папку проекта в пути Python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database import engine, SessionLocal, Base
from backend import models
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Form
from typing import Optional

# Создаем приложение FastAPI
app = FastAPI(title="Online Voting System")

# Настройка CORS для безопасности
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем все таблицы в базе данных при запуске
Base.metadata.create_all(bind=engine)

# Настраиваем пути к статическим файлам и шаблонам
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend", "templates")

# Монтируем папку со статическими файлами (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Настраиваем шаблонизатор Jinja2
templates = Jinja2Templates(directory=TEMPLATES_DIR)
class UserCreate(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user(request: Request, db: Session) -> Optional[models.User]:
    user_id = request.cookies.get("user_id")
    if user_id:
        return db.query(models.User).filter(models.User.id == int(user_id)).first()
    return None

def get_current_admin(request: Request, db: Session) -> Optional[models.User]:
    user = get_current_user(request, db)
    if user and user.is_admin:
        return user
    return None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    user = models.User(username=username, password=hash_password(password), is_admin=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Регистрация успешна", "user_id": user.id}

@app.post("/api/login")
def login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == username,
        models.User.password == hash_password(password)
    ).first()
    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    
    response.set_cookie(key="user_id", value=str(user.id))
    return {"message": "Вход выполнен", "is_admin": user.is_admin}

@app.get("/api/logout")
def logout(response: Response):
    response.delete_cookie("user_id")
    return {"message": "Выход выполнен"}

@app.get("/api/me")
def me(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return {"logged_in": False}
    return {"logged_in": True, "username": user.username, "is_admin": user.is_admin}

@app.get("/api/candidates")
def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    return candidates

@app.post("/api/vote/{candidate_id}")
def vote(candidate_id: int, request: Request, db: Session = Depends(get_db)):
    # Проверка авторизации
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Необходимо войти в систему")

    # Проверка: голосовал ли уже этот пользователь
    existing_vote = db.query(models.Vote).filter(
        models.Vote.user_id == user.id
    ).first()

    if existing_vote:
        raise HTTPException(
            status_code=400,
            detail="Вы уже голосовали! Один пользователь — один голос."
        )

    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")

    candidate.votes += 1

    # Сохраняем голос с привязкой к пользователю
    vote_record = models.Vote(
        user_id=user.id,
        candidate_id=candidate_id,
        user_ip=request.client.host  # для статистики, не для блокировки
    )
    db.add(vote_record)
    db.commit()

    return {
        "message": "Голос успешно учтен!",
        "candidate": candidate.name,
        "total_votes": candidate.votes
    }

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "candidates": candidates}
    )

@app.get("/results")
def results(request: Request, db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).order_by(
        models.Candidate.votes.desc()
    ).all()
    
    total_votes = sum(c.votes for c in candidates)
    max_votes = max(c.votes for c in candidates) if candidates else 0
    
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "candidates": candidates,
            "total_votes": total_votes,
            "max_votes": max_votes
        }
    )

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        candidates_count = db.query(models.Candidate).count()

        # Создаём админа по умолчанию
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            admin = models.User(username="admin", password=hash_password("admin123"), is_admin=True)
            db.add(admin)
            db.commit()
            print("Создан администратор: admin / admin123")
        
        if candidates_count == 0:
            print("База данных пуста. Добавляем тестовых кандидатов...")
            
            test_candidates = [
                models.Candidate(
                    name="Иван Петров",
                    description="Опытный руководитель с 10-летним стажем."
                ),
                models.Candidate(
                    name="Мария Сидорова",
                    description="Молодой специалист с инновационными идеями."
                ),
                models.Candidate(
                    name="Алексей Иванов",
                    description="Технический эксперт в области IT."
                ),
                models.Candidate(
                    name="Елена Кузнецова",
                    description="Социальный работник с 15-летним опытом."
                ),
                models.Candidate(
                    name="Дмитрий Соколов",
                    description="Предприниматель, создавший 500 рабочих мест."
                ),
            ]
            
            for candidate in test_candidates:
                db.add(candidate)
            
            db.commit()
            print(f"Успешно добавлено {len(test_candidates)} тестовых кандидатов!")
        else:
            print(f"В базе данных уже есть {candidates_count} кандидатов.")
            
    except Exception as e:
        print(f"Ошибка при инициализации данных: {e}")
        db.rollback()
    finally:
        db.close()
        
@app.post("/api/reset-votes")
def reset_votes(request: Request, db: Session = Depends(get_db)):
    admin = get_current_admin(request, db)
    if not admin:
        raise HTTPException(status_code=403, detail="Только для администратора")
    db.query(models.Vote).delete()
    db.query(models.Candidate).update({"votes": 0})
    db.commit()
    return {"message": "Все голоса сброшены"}

@app.get("/api/has-voted")
def has_voted(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return {"voted": False}
    vote = db.query(models.Vote).filter(models.Vote.user_id == user.id).first()
    return {"voted": vote is not None}

@app.get("/api/health")
def health_check():
    """Проверка работоспособности сервера"""
    return {"status": "ok", "message": "Сервер работает"}