from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Page, User, db  # Добавляем импорт db
from app import app
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Главная страница
@app.route('/')
def index():
    # Находим главную страницу по slug
    main_page = Page.query.filter((Page.slug == 'index') | (Page.slug == 'home')).first()
    return render_template('index.html', 
                         pages=Page.query.all(),
                         main_page=main_page)

# Страница по slug
@app.route('/<slug>')
def page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    return render_template('page.html', 
                         page=page,
                         pages=Page.query.all())  # Добавляем передачу pages

# Админ-панель (ДОБАВЛЯЕМ НОВЫЙ МАРШРУТ)
@app.route('/admin')
@login_required
def admin_panel():
    pages = Page.query.all()
    return render_template('admin/index.html', pages=pages)

# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('admin_panel'))  # Перенаправляем в админку
            
        flash('Неверные учетные данные', 'danger')
    return render_template('login.html', pages=Page.query.all())

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Создание страницы
@app.route('/admin/create', methods=['GET', 'POST'])
@login_required
def create_page():
    if request.method == 'POST':
        new_page = Page(
            title=request.form['title'],
            slug=request.form['slug'],
            content=request.form['content']
            )
        db.session.add(new_page)
        db.session.commit()
        flash('Страница успешно создана!', 'success')
        return redirect(url_for('admin_panel'))  # Перенаправляем в админку
    return render_template('admin/create.html',pages=Page.query.all())

# Редактирование страницы 
@app.route('/admin/edit/<int:page_id>', methods=['GET', 'POST'])
@login_required
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)
    if request.method == 'POST':
        page.title = request.form['title']
        page.slug = request.form['slug']
        page.content = request.form['content']
        db.session.commit()
        flash('Страница успешно обновлена!', 'success')
        return redirect(url_for('admin_panel'))  # Перенаправляем в админку   
    return render_template('admin/edit.html', page=page)

# Удаление страницы 
@app.route('/admin/delete/<int:page_id>', methods=['POST'])
@login_required
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    flash('Страница успешно удалена!', 'success')
    return redirect(url_for('admin_panel'))


