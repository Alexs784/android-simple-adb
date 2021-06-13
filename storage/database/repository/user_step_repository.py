from storage.database.database_manager import get_session
from storage.database.model.user_step import UserStep


def get_user_steps(user_step_command_id):
    session = get_session()
    user_steps = session.query(UserStep).filter(UserStep.command_id == user_step_command_id).all()
    session.close()
    return user_steps


def delete_user_steps(user_step_command_id):
    session = get_session()
    session.query(UserStep).filter(UserStep.command_id == user_step_command_id).delete()
    session.commit()
    session.close()


def get_grouped_user_steps_for_script(script_id):
    session = get_session()
    user_steps = session.query(UserStep) \
        .filter_by(script_id=script_id) \
        .group_by(UserStep.command_id) \
        .order_by(UserStep.time_created.asc()) \
        .all()
    session.close()
    return user_steps


def get_user_steps_for_script(script_id):
    session = get_session()
    user_steps = session.query(UserStep) \
        .filter_by(script_id=script_id) \
        .order_by(UserStep.time_created.asc()) \
        .all()
    session.close()
    return user_steps


def save_user_steps_in_database(user_steps):
    session = get_session()
    for user_step in user_steps:
        session.add(user_step)
    session.commit()
    session.close()
