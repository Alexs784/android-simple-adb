from sqlalchemy import Column, Integer, String

from storage.database.database_manager import Base


class UserScript(Base):
    __tablename__ = 'user_scripts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
