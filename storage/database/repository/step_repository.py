from storage.database.database_manager import get_session
from storage.database.model.step import Step


def get_steps():
    session = get_session()
    steps = session.query(Step).order_by(Step.name.asc()).all()
    session.close()
    return steps


def get_step_by_id(id):
    session = get_session()
    step = session.query(Step).filter_by(id=id).first()
    session.close()
    return step
