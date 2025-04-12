from app import app
from models import db, Page, User
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        print("Таблицы созданы")
        
        # Создаем администратора
        if not User.query.first():
            admin = User(
                username='admin',
                password=generate_password_hash('123')
            )
            db.session.add(admin)
            print("Создан администратор: admin/123")
        
        # Создаем базовые страницы
        if not Page.query.first():
            pages = [
                Page(title="Главная", slug="home", content="Добро пожаловать!"),
                Page(title="Контакты", slug="contacts", content="Телефон: ..."),
                Page(title="Галерея", slug="gallery", content="Фото будут здесь"),
                Page(title="Отзывы", slug="feedback", content="Отзывы клиентов")
            ]
            db.session.add_all(pages)
            print("Созданы базовые страницы")
        
        db.session.commit()
        print("✅ База данных успешно инициализирована!")

if __name__ == '__main__':
    init_database()