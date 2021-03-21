from sqlalchemy import Column, Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship

from storage.database.database_manager import Base
from storage.database.model.user_script import UserScript


class UserStep(Base):
    __tablename__ = 'user_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    command = Column(PickleType)
    command_id = Column(String)
    script_id = Column(Integer, ForeignKey('user_scripts.id'))

    UserScript.user_steps = relationship("UserStep", cascade="all, delete")


def get_user_step(name, command, command_id, script_id):
    return UserStep(name=name, command=command, command_id=command_id, script_id=script_id)
