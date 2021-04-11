from sqlalchemy import Column, Integer, String, ForeignKey, PickleType, DateTime, func
from storage.database.database_manager import Base


class UserStep(Base):
    __tablename__ = 'user_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    command = Column(PickleType)
    command_id = Column(String)
    script_id = Column(Integer, ForeignKey('user_scripts.id'))
    time_created = Column(DateTime(timezone=True), default=func.now())


def get_user_step(name, command, command_id, script_id):
    return UserStep(name=name, command=command, command_id=command_id, script_id=script_id)
