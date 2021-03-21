from storage.database.database_manager import get_session
from storage.database.model.user_step import UserStep


def get_user_steps_for_script(script_id):
    session = get_session()
    user_steps = session.query(UserStep) \
        .filter_by(script_id=script_id) \
        .group_by(UserStep.command_id) \
        .all()
    session.close()
    return user_steps


def save_user_step_in_database(user_step):
    session = get_session()
    session.add(user_step)
    session.commit()
    session.close()


def save_user_steps_in_database(user_steps):
    session = get_session()
    for user_step in user_steps:
        session.add(user_step)
    session.commit()
    session.close()
