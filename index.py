from flask import Flask, render_template, request, redirect, url_for, flash
from WORKOUT_PROJECT import app

from WORKOUT_PROJECT.init_db import db_session
from WORKOUT_PROJECT.db_table import User

from sqlalchemy.exc import SQLAlchemyError



@app.route('/test')
def home():
    SayHi = "운동기록 일지 서비스"
    return render_template('test.html', A = SayHi)


@app.route('/1')
def sqladd():
    session = db_session()
    try:
        test_user = User(user_id='test_user', user_pw='1234', user_name='test', user_email='test@example.com')
        session.add(test_user)
        session.commit()
        return 'User added successfully!'
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        return f'An error occurred: {error}'
    finally:
        session.clos



@app.route('/charts')
def charts():
    return render_template('charts.html')   
        
        
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/layout-sidenav')
def layout_sidenav():
    return render_template('layout-sidenav-light.html')

@app.route('/layout-static')
def layout_static():
    return render_template('layout-static.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/password')
def password():
    return render_template('password.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/tables')
def tables():
    return render_template('tables.html')








