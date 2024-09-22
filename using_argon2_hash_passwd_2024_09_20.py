import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from argon2 import PasswordHasher
from db_table import User


engine =create_engine("mysql+pymysql://root:930809@localhost/workoutrecord")
Session = sessionmaker(bind=engine)
session = Session()

ph = PasswordHasher()

def update_user_passwords():
    users = session.query(User).all()
    for user in users:
        original_password = user.user_pw  
        hashed_password = ph.hash(original_password)
        user.user_pw = hashed_password
    
    session.commit()
    print("All user passwords have been updated.")
    
if __name__ == "__main__":
    update_user_passwords()
    
    