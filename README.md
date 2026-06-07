# 🗳️ Система онлайн голосования

Веб-приложение для проведения онлайн голосования с авторизацией пользователей. Курсовой проект по дисциплине "Интернет-технологии".

## 🚀 Функциональность

- ✅ Регистрация и авторизация пользователей
- ✅ Разделение ролей (пользователь / администратор)
- ✅ Просмотр списка кандидатов с описанием
- ✅ Голосование (один пользователь — один голос)
- ✅ Блокировка повторного голосования
- ✅ Страница результатов с прогресс-барами
- ✅ Автообновление голосов в реальном времени (каждые 3 секунды)
- ✅ Сброс голосов (только для администратора)
- ✅ Уведомления по центру экрана
- ✅ Адаптивный дизайн (Bootstrap 5)
- ✅ Документация API (Swagger UI)
- ✅ Контейнеризация (Docker + Docker Compose + Nginx)
- ✅ Развертывание в облаке (SberCloud)

## 🛠️ Технологии

| Компонент | Технология |
|-----------|------------|
| Backend | Python 3.9, FastAPI, SQLAlchemy |
| База данных | SQLite (3 таблицы: users, candidates, votes) |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Авторизация | Cookies, SHA-256 |
| Контейнеризация | Docker, Docker Compose |
| Веб-сервер | Uvicorn + Nginx |
| Документация API | Swagger UI |
| Тестирование | Pytest (10 тестов) |
| Облако | SberCloud |

## 📦 Установка и запуск

### Данные по умолчанию

- **Администратор:** admin / admin123  
- **Кандидаты:** 5 тестовых кандидатов создаются автоматически

### Локальный запуск (Windows)

bash
# 1. Клонировать репозиторий
git clone https://github.com/Ditry-SD/Online-voting.git  
cd Online-voting

# 2. Создать и активировать виртуальное окружение
python -m venv venv  
venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить приложение
uvicorn backend.main:app --reload

После запуска открыть в браузере:  
http://localhost:8000 — главная страница  
http://localhost:8000/results  — результаты   
http://localhost:8000/docs — Swagger (описание API)

# Локальный запуск через Docker

# 1. Клонировать репозиторий
git clone https://github.com/Ditry-SD/online-voting.git  
cd online-voting

# 2. Собрать и запустить контейнер
docker-compose build  
docker-compose up  
или  
docker compose up -d --build  
docker-compose dowm (отключение)

После запуска открыть в браузере: http://localhost

# Развертывание на облачном сервере (SberCloud)

# 1. Подключиться к серверу по SSH
ssh user1@IP_адрес

# 2. Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh  
sudo sh get-docker.sh

# 3. Клонировать репозиторий
git clone https://github.com/Ditry-SD/Online-voting.git  
cd Online-voting

# 4. Создать файл базы данных
touch voting.db  
sudo chmod 777 voting.db

# 5. Запустить приложение
sudo docker compose up -d --build

Открыть в браузере: http://IP_адрес

# Запуск тестов

# Локально через Docker
docker compose run --rm web python -m pytest test/test_api.py -v

# На сервере
sudo docker compose run --rm web python -m pytest test/test_api.py -v

# 📡 API Endpoints
Метод	URL	Описание	Авторизация  
GET	/	Главная страница	Нет  
GET	/results	Результаты голосования	Нет  
POST	/api/register	Регистрация	Нет  
POST	/api/login	Вход в систему	Нет  
GET	/api/logout	Выход	Нет  
GET	/api/me	Данные пользователя	Нет  
GET	/api/candidates	Список кандидатов (JSON)	Нет  
POST	/api/vote/{id}	Голосование	Да  
GET	/api/has-voted	Проверка голосования	Да  
POST	/api/reset-votes	Сброс голосов	Админ  
GET	/api/health	Проверка сервера	Нет  
GET	/docs	Swagger UI	Нет

## 📁 Структура проекта

online-voting/  
├── backend/                    # Серверная часть приложения  
│   ├── __init__.py            # Инициализация Python-пакета  
│   ├── main.py                # Основной файл с API-эндпоинтами  
│   ├── models.py              # Модели таблиц базы данных (User, Candidate, Vote)  
│   └── database.py            # Настройка подключения к БД  
├── frontend/                   # Клиентская часть приложения  
│   ├── static/  
│   │   ├── css/  
│   │   │   └── style.css      # Стили оформления страниц  
│   │   └── js/  
│   │       └── voting.js      # Логика голосования (AJAX)  
│   └── templates/  
│       ├── index.html         # Главная страница  
│       └── results.html       # Страница результатов  
├── test/                       # Тесты  
│   └── test_api.py            # Модульные тесты API  
├── Dockerfile                  # Инструкция для сборки Docker-образа  
├── docker-compose.yml          # Конфигурация для Docker Compose  
├── nginx.conf                  # Конфигурация Nginx  
├── requirements.txt            # Список Python-зависимостей  
├── .dockerignore               # Исключения для Docker  
├── .gitignore                  # Игнорируемые Git файлы  
└── README.md                   # Описание проекта (этот файл)  

## 🌿 Стратегия ветвления (Git)

В проекте используется Git Flow:

main	Стабильная версия  
develop	Основная ветка разработки  
feature/auth-system	Авторизация и голосование  
feature/fixes	Фиксы интерфейса  
feature/tests	Модульные тесты  
feature/docker-improvements	Docker и Nginx  
feature/documentation	Документация  
feature/roles-and-security	Безопасность  

Порядок работы с ветками:

# Создание новой ветки от develop
git checkout develop  
git checkout -b feature/название

# ... внесение изменений ...
git add .  
git commit -m "описание"  
git checkout develop  
git merge --no-ff feature/название -m "merge: описание"  
git push origin develop

## 🔒 Система авторизации
Пароли хэшируются алгоритмом SHA-256

Сессии хранятся в cookies

Один пользователь — один голос

Администратор может сбрасывать голоса

## 📊 Страница результатов

Голоса обновляются автоматически каждые 3 секунды через AJAX-запросы.  
При изменении данных счётчики анимируются. Страница результатов  
перерисовывает прогресс-бары при обнаружении изменений.

## Схема базы данных

candidates  
├── id (INTEGER, PK)  
├── name (VARCHAR, UNIQUE)  
├── description (VARCHAR)  
└── votes (INTEGER)  

votes  
├── id (INTEGER, PK)  
├── user_ip (VARCHAR, INDEXED)  
├── candidate_id (INTEGER, FK)  
└── timestamp (DATETIME)

## 🌐 Демонстрация
Приложение развернуто в облаке SberCloud:  
http://ip

## 👨‍💻 Автор
ФИО: Морозов Дмитрий Владимирович  
Группа: ПИН-б-з-22-1  
Дисциплина: Интернет-технологии  
Год: 2026
