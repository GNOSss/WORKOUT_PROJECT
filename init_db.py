from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base


# db_url 구문 끝에 ?charset=utf8 생략 후 실행
db_url = "mysql+pymysql://root:930809@localhost/workoutrecord"

db_engine = create_engine(db_url, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind = db_engine))

db_Base = declarative_base()
db_Base.query = db_session.query_property()



def init_database():
    import WORKOUT_PROJECT.db_table
    db_Base.metadata.create_all(db_engine)

    



# # UserPhysical 테이블의 user_of_birth 컬럼 추가
# from sqlalchemy import text
# # db_engine 연결
# with db_engine.connect() as conn:
#     # execute(text())활용하여 쿼리문 날리기
#     conn.execute(text("ALTER TABLE UserPhysical ADD COLUMN user_of_birth DATE NOT NULL"))    
#     conn.commit()
