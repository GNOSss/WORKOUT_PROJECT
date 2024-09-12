from WORKOUT_PROJECT.init_db import db_Base
from sqlalchemy import Column, VARCHAR, DECIMAL, TIMESTAMP, INTEGER, Float, Boolean, Date, DateTime
from sqlalchemy.orm import relationship, backref 
from sqlalchemy import ForeignKey


class User(db_Base):
    __tablename__ = 'User'
    
    user_id = Column(VARCHAR(20), primary_key=True)
    user_pw = Column(VARCHAR(100), nullable=False)
    user_name = Column(VARCHAR(20), nullable=False)
    user_email = Column(VARCHAR(100))
    
    def __init__(self, user_id=None, user_pw=None, user_name=None, user_email=None):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_name = user_name
        self.user_email = user_email
    
    def __repr__(self):
        return f'User(user_id={self.user_id}, user_pw={self.user_pw}, user_name={self.user_name}, user_email={self.user_email})'
    
    
    
class UserPhysical(db_Base):
    __tablename__ = 'UserPhysical'
    
    user_id = Column(VARCHAR(20), ForeignKey('User.user_id'), primary_key=True)
    user_height = Column(DECIMAL(5,2))
    user_weight = Column(DECIMAL(5,2))
    user_of_birth = Column(Date, nullable=False)
    recorded_time = Column(TIMESTAMP, primary_key=True)
    user = relationship("User", backref="usertouserphysical")
    
    def __init__(self, user_id=None, user_height=None, user_weight=None, user_of_birth=None, recorded_time=None):
        self.user_id = user_id
        self.user_height = user_height
        self.user_weight = user_weight
        self.user_of_birth = user_of_birth
        self.recorded_time = recorded_time
    
    def __repr__(self):
        return f'UserPhysical(user_id={self.user_id}, user_height={self.user_height}, user_weight={self.user_weight}, user_of_birth={self.user_of_birth} ,recorded_time={self.recorded_time})'
    
    
    
class WhatKindWorkOut(db_Base):
    __tablename__ = 'WhatKindWorkOut'
    
    workout_name = Column(VARCHAR(100), ForeignKey('Routine.workout_name'), primary_key=True)
    region = Column(VARCHAR(50))
    info = Column(VARCHAR(2000))
    your_record = Column(VARCHAR(100))
    routine = relationship("Routine", backref="routinetowhatkinworkout")    
    
    def __init__(self, workout_name=None, region=None, info=None, your_record=None):
        self.workout_name = workout_name
        self.region = region
        self.info = info
        self.your_record = your_record
        
    def __repr__(self):
        return f'WhatKindWorkOut(workout_name={self.workout_name}, region={self.region}, info={self.info}, your_record={self.your_record})'
    


class Routine(db_Base):    
    __tablename__ = 'Routine'
    
    template_name = Column(VARCHAR(100), primary_key=True)
    user_id = Column(VARCHAR(20), ForeignKey('User.user_id') ,nullable=False)
    routine_name = Column(VARCHAR(100), nullable=False, index=True)
    workout_name = Column(VARCHAR(100), nullable=False, index=True)
    user = relationship("User", backref="usertoroutine")
    
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
    routine = relationship("Routine", backref="routinetodailyrecord")
    
    def __init__(self, today=None, routine_name=None, workout_name=None, weight=None, count=None):
        self.today = today
        self.routine_name = routine_name
        self.workout_name = workout_name
        self.weight = weight
        self.count = count
    
    def __repr__(self):
        return f'DailyRecord(today={self.today}, routine_name={self.routine_name}, workout_name={self.workout_name}, weight={self.weight}, count={self.count})'
    


class UserRecord(db_Base):
    __tablename__ = 'UserRecord'
    
    workout_name = Column(VARCHAR(100), ForeignKey('WhatKindWorkOut.workout_name'), primary_key=True)
    today = Column(TIMESTAMP, ForeignKey('DailyRecord.today'), primary_key=True)
    weight = Column(DECIMAL(5,2))
    count = Column(INTEGER)
    workout = relationship("WhatKindWorkout", back_populates="user_records")
    daily_record = relationship("DailyRecord", back_populates="user_records")
    
    
    def __init__(self, workout_name=None, today=None, weight=None, count=None):
        self.workout_name=workout_name
        self.today = today
        self.weight = weight
        self.count = count
    
    def __repr__(self):
        return f'UserRecord(workout_name={self.workout_name}, today={self.today}, weight={self.weight}, count={self.count})'
    



    