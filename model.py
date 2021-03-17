from sqlalchemy import String, Integer, Column, Boolean
from database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_member = Column(Boolean, default=False)
