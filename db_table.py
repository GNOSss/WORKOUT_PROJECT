from WORKOUT_PROJECT.init_db import db_Base
from sqlalchemy import Column, VARCHAR, DECIMAL, TIMESTAMP, INTEGER, Float, Boolean, Date, DateTime
from sqlalchemy.orm import relationship, backref 
from sqlalchemy import ForeignKey
from argon2 import PasswordHasher
from flask_login import UserMixin


class User(UserMixin, db_Base):
    __tablename__ = 'User'
    
    user_id = Column(VARCHAR(20), primary_key=True)
    user_pw = Column(VARCHAR(255), nullable=False)  # argon2 해시함수 사용하기 위해 (100)에서 (255)로 늘림
    user_name = Column(VARCHAR(20), nullable=False)
    user_email = Column(VARCHAR(100))
    
    user_physicals = relationship("UserPhysical", back_populates="user")
    routines = relationship("Routine", back_populates="user")
    
    def __init__(self, user_id=None, user_pw=None, user_name=None, user_email=None):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_name = user_name
        self.user_email = user_email
        
    def get_id(self):
        return str(self.user_id)
    
    # Argon2 해시 함수 적용 코드    
    def set_password(self, password):
        ph = PasswordHasher()
        self.user_pw = ph.hash(password)

    # Argon2 해시 함수 적용 코드        
    def check_password(self, password):
        ph = PasswordHasher()
        return ph.verify(self.user_pw, password)
    
    def __repr__(self):
        return f'User(user_id={self.user_id}, user_pw={self.user_pw}, user_name={self.user_name}, user_email={self.user_email})'
    
    
    
class UserPhysical(db_Base):
    __tablename__ = 'UserPhysical'
    
    user_id = Column(VARCHAR(20), ForeignKey('User.user_id'), primary_key=True)
    user_height = Column(DECIMAL(5,2))
    user_weight = Column(DECIMAL(5,2))
    user_of_birth = Column(Date, nullable=False)
    recorded_time = Column(TIMESTAMP, primary_key=True)
    
    user = relationship("User", back_populates="user_physicals")

    
    def __init__(self, user_id=None, user_height=None, user_weight=None, user_of_birth=None, recorded_time=None):
        self.user_id = user_id
        self.user_height = user_height
        self.user_weight = user_weight
        self.user_of_birth = user_of_birth
        self.recorded_time = recorded_time
    
    def __repr__(self):
        return f'UserPhysical(user_id={self.user_id}, user_height={self.user_height}, user_weight={self.user_weight}, user_of_birth={self.user_of_birth} ,recorded_time={self.recorded_time})'
    
    
    
class UserRecord(db_Base):
    __tablename__ = 'UserRecord'
    
    workout_name = Column(VARCHAR(100), ForeignKey('WhatKindWorkOut.workout_name'), primary_key=True)
    today = Column(TIMESTAMP, ForeignKey('DailyRecord.today'), primary_key=True)
    weight = Column(DECIMAL(5,2))
    count = Column(INTEGER)
    
    workout = relationship("WhatKindWorkOut", back_populates="user_records")
    daily_record = relationship("DailyRecord", back_populates="user_records")
    
    def __init__(self, workout_name=None, today=None, weight=None, count=None):
        self.workout_name=workout_name
        self.today = today
        self.weight = weight
        self.count = count
    
    def __repr__(self):
        return f'UserRecord(workout_name={self.workout_name}, today={self.today}, weight={self.weight}, count={self.count})'    
    
    
class WhatKindWorkOut(db_Base):
    __tablename__ = 'WhatKindWorkOut'
    
    workout_id = Column(INTEGER, primary_key=True, autoincrement=True)
    workout_name = Column(VARCHAR(100), index=True)
    region = Column(VARCHAR(50))
    equipment = Column(VARCHAR(50))
    info = Column(VARCHAR(2000))
    
    routines = relationship("Routine", back_populates="workout_type")
    user_records = relationship("UserRecord", back_populates="workout")
    
    def __init__(self, workout_name=None, region=None, equipment=None, info=None):
        self.workout_name = workout_name
        self.region = region
        self.equipment = equipment
        self.info = info
        
    def __repr__(self):
        return f'WhatKindWorkOut(workout_name={self.workout_name}, region={self.region},equipment={self.equipment} , info={self.info})'
    


class Routine(db_Base):    
    __tablename__ = 'Routine'
    
    routine_id = Column(INTEGER, primary_key=True, autoincrement=True)
    template_name = Column(VARCHAR(100), nullable=False)
    user_id = Column(VARCHAR(20), ForeignKey('User.user_id') ,nullable=False)
    routine_name = Column(VARCHAR(100), nullable=False, index=True)
    workout_name = Column(VARCHAR(100), ForeignKey('WhatKindWorkOut.workout_name'), nullable=False)
    
    user = relationship("User", back_populates="routines")
    workout_type = relationship("WhatKindWorkOut", back_populates="routines")
    daily_records = relationship("DailyRecord", back_populates="routine")
    
    
    def __init__(self, template_name=None, user_id=None, routine_name=None, workout_name=None):
        self.template_name = template_name
        self.user_id = user_id
        self.routine_name = routine_name
        self.workout_name = workout_name
        
    def __repr__(self):
        return f'Routine(template_name={self.template_name}, user_id={self.user_id}, routine_name={self.routine_name}, workout_name={self.workout_name})'
    
    
    
class DailyRecord(db_Base):
    __tablename__ = 'DailyRecord'
    
    today = Column(TIMESTAMP, primary_key=True)
    routine_name = Column(VARCHAR(100), ForeignKey('Routine.routine_name'))
    workout_name = Column(VARCHAR(100))
    weight = Column(DECIMAL(5,2))
    count = Column(INTEGER)
    
    routine = relationship("Routine", back_populates="daily_records")
    user_records = relationship("UserRecord", back_populates="daily_record")

    
    def __init__(self, today=None, routine_name=None, workout_name=None, weight=None, count=None):
        self.today = today
        self.routine_name = routine_name
        self.workout_name = workout_name
        self.weight = weight
        self.count = count
    
    def __repr__(self):
        return f'DailyRecord(today={self.today}, routine_name={self.routine_name}, workout_name={self.workout_name}, weight={self.weight}, count={self.count})'
    


    