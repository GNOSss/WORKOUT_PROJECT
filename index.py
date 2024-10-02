from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from WORKOUT_PROJECT import app
from WORKOUT_PROJECT.init_db import db_session
from WORKOUT_PROJECT.db_table import User, UserPhysical, WhatKindWorkOut, Routine, DailyRecord
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, datetime
from sqlalchemy import desc, or_, distinct
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
# current_user는 현재 사용자를 나타내는 객체 ,  로그인 된 경우 사용자의 정보를 담을 것이고, 로그인되지 않는 경우 AnonymousUserMixin은 상속받아 익명 사용자 객체로 됨



# csv파일 DB에 입력하기 위해
import pandas as pd


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', username=current_user.user_name)
    return render_template('index.html')






@app.route('/myprofile', methods=['GET'])
# @login_required를 통해 /myprofile은 로그인한 사용자만 접근 할 수 있음
# 로그인 되어 있지 않는다면 __init__.py에서 login_manager.login_view = 'login' 이 코드를 통해 'login'페이지로 이동하게 됨
@login_required
def myprofile():
    print(f"Current user: {current_user.user_id}")  # 로그 추가
    user_physicals = UserPhysical.query.filter_by(user_id=current_user.user_id).order_by(UserPhysical.recorded_time.desc()).all()
    print(f"User physicals: {user_physicals}")  # 로그 추가
    return render_template('myprofile.html', user_physicals=user_physicals)

@app.route('/add_physical', methods=['POST'])
@login_required
def add_physical():
    try:
        height = request.form.get('height')
        weight = request.form.get('weight')
        birthdate = request.form.get('birthdate')
        
        new_physical = UserPhysical(
            user_id = current_user.user_id,
            user_height = height,
            user_weight = weight,
            user_of_birth = datetime.strptime(birthdate, '%Y-%m-%d').date(),
            recorded_time=datetime.now()
        )
        
        db_session.add(new_physical)
        db_session.commit()
        
        return jsonify({"ok":True})
    
    except SQLAlchemyError as e:
        return jsonify({"success": False, "error": str(e)})
    
    
@app.route('/delete_physical/<string:user_id>/<string:recorded_time>', methods=['DELETE'])
@login_required
def delete_physical(user_id, recorded_time):
    try:
        # 현재 로그인한 사용자의 ID와 요청된 user_id가 일치하는지 확인
        if current_user.user_id != user_id:
            return jsonify({'success': False, 'error': 'Permission denied'}), 403

        # recorded_time을 datetime 객체로 변환
        recorded_time = datetime.strptime(recorded_time, '%Y-%m-%d %H:%M:%S')

        physical_record = UserPhysical.query.filter_by(user_id=user_id, recorded_time=recorded_time).first()
        if physical_record:
            db_session.delete(physical_record)
            db_session.commit()
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
    except Exception as e:
        db_session.rollback()
        print(f"Error deleting record: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/update_physical/<string:user_id>/<string:recorded_time>', methods=['PUT'])
@login_required
def update_physical(user_id, recorded_time):
    try:
        if current_user.user_id != user_id:
            return jsonify({'success': False, 'error': 'Permission denied'}), 403

        recorded_time = datetime.strptime(recorded_time, '%Y-%m-%d %H:%M:%S')
        physical_record = UserPhysical.query.filter_by(user_id=user_id, recorded_time=recorded_time).first()

        if physical_record:
            physical_record.user_height = request.json.get('height', physical_record.user_height)
            physical_record.user_weight = request.json.get('weight', physical_record.user_weight)
            physical_record.user_of_birth = datetime.strptime(request.json.get('birthdate', physical_record.user_of_birth.strftime('%Y-%m-%d')), '%Y-%m-%d').date()

            db_session.commit()
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
    except Exception as e:
        db_session.rollback()
        print(f"Error updating record: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500







@app.route('/routine', methods=['GET'])
@login_required
def routine():
    # 현재 사용자의 고유한 템플릿 이름 가져오기
    templates = db_session.query(distinct(Routine.template_name)).filter_by(user_id=current_user.user_id).all()
    templates = [t[0] for t in templates]  # 튜플에서 문자열로 변환
    
    return render_template('routine.html', templates=templates)

@app.route('/get_routines/<template_name>', methods=['GET'])
@login_required
def get_routines(template_name):
    routines = db_session.query(distinct(Routine.routine_name)).filter_by(user_id=current_user.user_id, template_name=template_name).all()
    routines = [r[0] for r in routines]  # 튜플에서 문자열로 변환
    return jsonify(routines)


@app.route('/get_workouts/<template_name>/<path:routine_name>', methods=['GET'])
@login_required
def get_workouts(template_name, routine_name):
    print(f"Fetching workouts for template: {template_name}, routine: {routine_name}")
    workouts = db_session.query(Routine.workout_name).filter_by(user_id=current_user.user_id, template_name=template_name, routine_name= routine_name).group_by(Routine.workout_name).all()
    # workouts = Routine.query.filter_by(user_id=current_user.user_id, template_name=template_name, routine_name=routine_name).all()
    workout_list = [{'workout_name': w.workout_name} for w in workouts]
    print(f"Found workouts: {workout_list}")
    return jsonify(workout_list)



# 신체 부위
@app.route('/workout/<region>')
@login_required
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
@login_required
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
@login_required
def charts():
    return render_template('charts.html')

# 나의 기록
@app.route('/myrecoard')
def myrecoard():
    return render_template('myrecoard.html',)



# 로그인
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login_post():
    ph = PasswordHasher()
    
    id = request.form.get('id')
    passwd = request.form.get('passwd')
    
    print(f"Attempting login for user: {id}")  # 디버깅용 출력
    
    user = User.query.filter_by(user_id=id).first()
    if user:
        print(f"User found: {user.user_id}")
        print(f"Stored password hash: {user.user_pw}")  # 저장된 해시 출력
        try:
            if ph.verify(user.user_pw, passwd):
                # login_user의 user는 User 테이블의 UserMixin은 상속받아야함, remember는 브라우저 닫아도 로그인상태 유지 , duration은 로그인상태 유지 기간 설정함, 그외 force, fresh 기능있음
                login_user(user, remember=True)
                print('User login successful')
                return redirect(url_for('index'))
            else:
                print("Password verification failed")  # 디버깝용 출력
        except VerifyMismatchError:
            print("Password mismatch")  # 디버깅용 출력
        except InvalidHash:
            print("Invalid hash format")
        except Exception as e:
            print(f"An error occurred: {str(e)}")  # 디버깅용 출력
    else:
        print(f"No user found with id: {id}")  # 디버깅용 출력
        
    flash('Invalid username or password')
    print('Login Failed')
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



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



# 테스트용 루틴 데이터 입력
@app.route('/create_sample_routines', methods=['GET'])
def create_sample_routines():
    session = db_session()
    try:
        # 샘플 루틴 데이터
        sample_routines = [
            {'template_name': '2분할', 'routine_name': '밀기', 'workouts': ['Bench Press', 'Incline Dumbbell Press', 'Shoulder Press', 'Lateral Raises']},
            {'template_name': '2분할', 'routine_name': '당기기', 'workouts': ['Pull-ups', 'Barbell Row', 'Squats', 'Leg Press']},
        ]

        for routine in sample_routines:
            for workout in routine['workouts']:
                # 운동이 WhatKindWorkOut 테이블에 있는지 확인
                workout_exists = session.query(WhatKindWorkOut).filter_by(workout_name=workout).first()
                if not workout_exists:
                    # 없으면 새로 추가 (실제 환경에서는 이 부분을 더 정교하게 처리해야 합니다)
                    new_workout = WhatKindWorkOut(workout_name=workout, region='Unknown', equipment='Unknown', info='Sample workout')
                    session.add(new_workout)

                new_routine = Routine(
                    template_name=routine['template_name'],
                    user_id='testuser12',
                    routine_name=routine['routine_name'],
                    workout_name=workout
                )
                session.add(new_routine)

        session.commit()
        return jsonify({'message': 'Sample routines created successfully for testuser12'}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


