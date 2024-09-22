from WORKOUT_PROJECT.init_db import db_session
from flask import Flask
from WORKOUT_PROJECT.init_db import init_database
from flask_login import LoginManager, current_user
from .db_table import User
import os


app = Flask(__name__)
# Remember me 기능을 위해서 10,11번째줄 작성
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = os.urandom(24)
app.debug = True




@app.context_processor
def inject_user():
    return dict(current_user=current_user)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
import WORKOUT_PROJECT.index


# 애플리케이션 생성 시점에 초기화 코드 실행
# flask 2.3 이전에는 @app.before_first_request  사용 했었음
def create_app():
    app = Flask(__name__)
    
    # 초기화 코드
    print(">> before first request")
    init_database()
    
    return app



# 모든 요청 처리 후 응답 수정
@app.after_request
def afterReq(response):
    print(">> after request")
    return response


# 리스폰스 처리 완료 후 리소스 정리
@app.teardown_request
def teardown_request(exception):
    print(">> teardown request", exception)
    

# 애플리케이션 컨텍스트 종료 시 리소스 정리
# 그렇지 않으면 DB에 세션이 계속해서 생성 될 수 있다.
@app.teardown_appcontext
def teardown_context(exception):
    print(">> teardown context", exception)
    db_session.remove()