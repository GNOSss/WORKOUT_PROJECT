from flask import Flask, render_template, request, redirect, url_for, flash
from WORKOUT_PROJECT import app

from WORKOUT_PROJECT.init_db import db_session
from WORKOUT_PROJECT.db_table import User

from sqlalchemy.exc import SQLAlchemyError



@app.route('/')
def home():
    SayHi = "운동기록 일지 서비스"
    return render_template('index.html', A = SayHi)


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
        session.close()