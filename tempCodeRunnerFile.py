class User(db_Base):
    __tablename__ = 'User'
    
    user_id = Column(VARCHAR(20), primary_key=True)
    user_pw = Column(VARCHAR(100), nullable=False)
    user_name = Column(VARCHAR(20), nullable=False)
    user_email = Column(VARCHAR(100))
    
    user_physicals = relationship("UserPhysical", back_populates="user")
    routines = relationship("Routine", back_populates="user")
    
    def __init__(self, user_id=None, user_pw=None, user_name=None, user_email=None):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_name = user_name
        self.user_email = user_email
    
    def __repr__(self):
        return f'User(user_id={self.user_id}, user_pw={self.user_pw}, user_name={self.user_name}, user_email={self.user_email})'
    