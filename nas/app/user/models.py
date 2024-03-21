from hmac import compare_digest
from sqlalchemy import Column, Integer, String
from .. import db

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'sys_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username  = Column(String, nullable=False, unique=True)
    password  = Column(String, nullable=False)
    email = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    def check_password(self, password):
        return compare_digest(password, self.password)