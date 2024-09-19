from flask import Flask, render_template, request, redirect, url_for, flash, abort
from WORKOUT_PROJECT import app
from WORKOUT_PROJECT.init_db import db_session
from WORKOUT_PROJECT.db_table import User, UserPhysical, WhatKindWorkOut, Routine, DailyRecord
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, datetime
from sqlalchemy import desc, or_

# csv파일 DB에 입력하기 위해
import pandas as pd




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/routine')
def routine():
    return render_template('routine.html')



# 신체 부위
@app.route('/workout/<region>')
def workout_route(region):
    
    # URL 매개변수 region의 객체가 아래 8개 중에 있는지 검사
    valid_regions = {'chest', 'back', 'leg', 'shoulder', 'arm', 'body', 'cardio', 'etc'}
    if region.lower() not in valid_regions:    
        abort(404, description="Invalid workout region")
    
    # URL 매개변수 region을 .capitalize() 첫글자 대문자화 , db_session 연결하고 get_workouts_by_region함수 호출하여 DB에서 데이터 추출
    workouts = get_workouts_by_region(region.capitalize(), db_session)
    if workouts is None:
        abort(500, description="An error occurred while fetching workouts")
    
    # get_workouts_by_region에서 받아온 결과 값(workouts)과 region을 html로 반환 , 이때 capitalize()했던 값을 다시 .lower()처리
    # return render_template(f'workout/wo_{region.lower()}.html', workouts=workouts, region=region)
    return render_template('workout/workout.html', workouts=workouts, region=region)


def get_workouts_by_region(region, session):
    try:
        # get_workouts_by_region함수에 region = WhatKindWorkOut테이블의 컬럼명, session은 db_session 역할을 하게 됨
        return session.query(WhatKindWorkOut).filter(WhatKindWorkOut.region == region).all()
    except SQLAlchemyError as e:
        print(f"Error fetching {region} workouts: {e}")
        return None






# 기구 카테고리
@app.route('/equipment/<equipment>')
def equipment_route(equipment):
    
    # URL 매개변수 equipment의 객체가 아래 5개 중에 있는지 검사
    valid_equipments = {'barbel', 'dumbel', 'machine', 'body', 'etc'}
    if equipment not in valid_equipments:
        return "Invalid equipment type", 400
    
    # URL 매개변수 equipment를 .capitalize() 첫글자 대문자화, db_session 연결하고 get_workouts_by_equipment함수 호출하여 DB에서 데이터 추출
    workouts = get_workouts_by_equipment(equipment, db_session)
    if workouts is None:
        return abort(500, description="An error occurred while fetching workouts")
    
    # get_workouts_by_equipment에서 받아온 결과 값(workouts)와 equipment를 html로 반환, 이때 capitalize()했던 값을 다시.lower()처리
    # return render_template(f'equipment/eq_{equipment}.html', workouts=workouts)
    return render_template('equipment/equipment.html', workouts=workouts, equipmnet=equipment)


def get_workouts_by_equipment(equipment, session):
    try:
        workouts = session.query(WhatKindWorkOut).filter(WhatKindWorkOut.equipment == equipment)\
                                                    .order_by(WhatKindWorkOut.region, WhatKindWorkOut.workout_name).all()
        return workouts
    except SQLAlchemyError as e:
        print(f"Error fetching {equipment} workouts: {e}")
        return None
    




# 차트
@app.route('/charts')
def charts():
    return render_template('charts.html')

# 나의 기록
@app.route('/myrecoard')
def myrecoard():
    return render_template('myrecoard.html',)



# 로그인
@app.route('/login')
def login():
    return render_template('login.html')

# 비밀번호 찾기
@app.route('/password')
def password():
    return render_template('password.html')

# 회원가입
@app.route('/register')
def register():
    return render_template('register.html')




# 공통 레이아웃
@app.route('/layout-sidenav')
def layout_sidenav():
    return render_template('layout-sidenav-light.html')

@app.route('/layout-static')
def layout_static():
    return render_template('layout-static.html')



# 에러 페이지

@app.errorhandler(401)
def for_zero_one(error):
    return render_template('401.html'),401        

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'),500


# 에러 테스트 라우트
@app.route('/test-401')
def test_401():
    abort(401) #abort : 의도적으로 에러 발생하는 함수
    
@app.route('/test-404')
def test_404():
    abort(404) #abort : 의도적으로 에러 발생하는 함수

@app.route('/test-500')
def test_500():
    # 의도적으로 오류 발생
    raise Exception("This is a test 500 error")




@app.route('/1')
def sqladd():
    session = db_session()
    
    
    # # UserPhysical 일부 데이터 삭제
    # try:
    #     poppop = session.query(UserPhysical).order_by(desc(UserPhysical.recorded_time)).first()
    #     if poppop:
    #         session.delete(poppop)
    #         session.commit()
    #     return '삭제 완료'
    # except SQLAlchemyError as e:
    #     session.rollback()
    #     error = str(e.__dict__['orig'])
    #     return f'An error occurred: {error}'
    # finally:
    #     session.close()
    
    
    # # UserPhysical 테스트 생성
    # try:
    #     test_userphysical = UserPhysical(user_id='test_user2', user_height='190', user_weight='99',user_of_birth=date(1988,12,18), recorded_time=datetime.now())
    #     session.add(test_userphysical)
    #     session.commit()
    #     return '유저 신체정보 입력완성'
    
    # except SQLAlchemyError as e:
    #     session.rollback()
    #     error = str(e)
    #     return f'An error occurred: {error}'    
        
    # finally:
    #     session.close()        
    
    
    # User 테스트 생성
    # try:
    #     for i in range(2,11):
    #         user_id = f'test_user{i}'
    #         user_pw = '1234'
    #         user_name = f'test{i}'
    #         user_email = f'test{i}@example.com'
    
    #         test_user = User(user_id=user_id, user_pw=user_pw, user_name=user_name, user_email=user_email)
    #         session.add(test_user)
    #     session.commit()
    #     return 'User added successfully!'
    # except SQLAlchemyError as e:
    #     session.rollback()
    #     error = str(e)
    #     return f'An error occurred: {error}'
    # finally:
    #     session.close()
    
    
    # WhatKindWorkOut 테스트 생성
    # datafile = pd.read_csv('WORKOUT_PROJECT/workoutsample.csv')
    # try:      
    #     for _, row in datafile.iterrows():
    #         workout = WhatKindWorkOut(
    #             workout_name=row['workout_name'],
    #             region=row['region'],
    #             equipment=row['equipment'],
    #             info=row['info']
    #         )
    #         session.add(workout)
    #     session.commit()
    #     return 'workout 입력완료!'
    
    # except SQLAlchemyError as e:
    #     session.rollback()
    #     error = str(e)
    #     return f'An error occurred: {error}'
    # finally:
    #     session.close()


    # Routine 테스트 생성
    # try:
    #     workout_names = ['Overhead Press', 'Shoulder Press', 'Lateral Raise', 'Face Pull', 'Arnold Press']
        
    #     template_name = '4분할'
    #     user_id = 'test_user1'
    #     routine_name = '어깨'
        
    #     for workout_name in workout_names:
    #         new_routine = Routine(
    #             template_name=template_name,
    #             user_id=user_id,
    #             routine_name=routine_name,
    #             workout_name=workout_name
    #         )        
    #         session.add(new_routine)
    #     session.commit()
    #     return '유저 루틴 입력완성'
    
    # except SQLAlchemyError as e:
    #     session.rollback()
    #     error = str(e)
    #     return f'An error occurred: {error}'    
        
    # finally:
    #     session.close()        
    

@app.route('/test')
def home():
    SayHi = "운동기록 일지 서비스"
    return render_template('test.html', A = SayHi)



