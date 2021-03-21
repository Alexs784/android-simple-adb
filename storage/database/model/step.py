from sqlalchemy import Column, Integer, String, PickleType

from storage.database.database_manager import Base


class Step(Base):
    __tablename__ = 'steps'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    commands = Column(PickleType)
    parameters_names = Column(PickleType)
    parameters_descriptions = Column(PickleType)


def get_step(name, commands, parameters_names, parameters_descriptions):
    return Step(
        name=name,
        commands=commands,
        parameters_names=parameters_names,
        parameters_descriptions=parameters_descriptions
    )
