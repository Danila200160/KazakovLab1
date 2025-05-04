from flask import Flask, request, g
from flask_login import LoginManager
from flask_caching import Cache
import time
from collections import deque

from models import db

# Инициализация приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Настройка кеширования (simple cache для разработки)
app.config.update({
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 60  # Таймаут кеша по умолчанию в секундах
})
cache = Cache(app)

# Инициализация базы данных
db.init_app(app)

# Настройка Flask-Login
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Лог запросов и замеры времени
request_log = deque(maxlen=50)

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_and_set_cache_headers(response):
    # Замер времени выполнения запроса
    if hasattr(g, 'start'):
        duration = time.time() - g.start
        request_log.appendleft({'path': request.path, 'time': duration})
        print(f"[TIME] {request.path} — {duration:.4f}s")
    # Добавляем HTTP-заголовки кеширования для статических файлов
    if request.path.startswith('/static/'):
        response.cache_control.public = True
        response.cache_control.max_age = 86400  # 1 день
    return response

# Инициализация и миграция базы данных

def initialize_app():
    with app.app_context():
        db.create_all()
        from models import User, Page
        if not User.query.first():
            from werkzeug.security import generate_password_hash
            admin = User(username='admin', password=generate_password_hash('123'))
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    initialize_app()
    from routes import *
    app.run(debug=True, host='0.0.0.0')
