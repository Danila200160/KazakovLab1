from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
from models import db
db.init_app(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

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
    from routes import *  # Импорт маршрутов после инициализации
    app.run(debug=True)