from storage.database.database_manager import get_session
from storage.database.model.user_step import UserStep


def get_user_steps(user_step_command_id):
    session = get_session()
    user_steps = session.query(UserStep).filter(UserStep.command_id == user_step_command_id).all()
    session.close()
    return user_steps


def delete_user_steps(user_step_command_id, script_id):
    session = get_session()
    user_steps = session.query(UserStep) \
        .filter(UserStep.command_id == user_step_command_id) \
        .all()

    deleted_position = -1
    for user_step in user_steps:
        deleted_position = user_step.position
        session.delete(user_step)

    if deleted_position != -1:
        session.query(UserStep).filter_by(script_id=script_id) \
            .filter(UserStep.position > deleted_position) \
            .update({"position": UserStep.position - 1}, synchronize_session=False)

    session.commit()
    session.close()


def get_grouped_user_steps_for_script(script_id):
    session = get_session()
    user_steps = session.query(UserStep) \
        .filter_by(script_id=script_id) \
        .group_by(UserStep.command_id) \
        .order_by(UserStep.position.asc()) \
        .all()
    session.close()
    return user_steps


def get_user_steps_for_script(script_id):
    session = get_session()
    user_steps = session.query(UserStep) \
        .filter_by(script_id=script_id) \
        .order_by(UserStep.position.asc()) \
        .all()
    session.close()
    return user_steps


def save_user_steps_in_database(user_steps):
    existing_grouped_user_steps = get_grouped_user_steps_for_script(user_steps[0].script_id)
    if existing_grouped_user_steps is None:
        position_offset = 0
    else:
        position_offset = len(existing_grouped_user_steps)

    grouped_user_steps_to_save = {}
    for user_step in user_steps:
        if user_step.command_id not in grouped_user_steps_to_save:
            grouped_user_steps_to_save[user_step.command_id] = []
        grouped_user_steps_to_save[user_step.command_id].append(user_step)

    session = get_session()
    for group_index, (command_id, user_steps) in enumerate(grouped_user_steps_to_save.items()):
        for user_step in user_steps:
            position = group_index + position_offset
            user_step.position = position
            print((f"Saving user step {user_step.name} with command:\n{user_step.command}\nand position {position}"))
            session.add(user_step)

    session.commit()
    session.close()


def update_user_step_position(id, new_position):
    session = get_session()

    # Fetch the item to be moved
    user_step = session.query(UserStep).filter(UserStep.id == id).first()
    old_position = user_step.position

    # Check if the position is actually changing
    if new_position != old_position:
        # Determine the direction of the move and update positions accordingly
        if new_position < old_position:
            # Moving backward: Increment positions of items between new and old positions
            session.query(UserStep).filter(
                UserStep.position >= new_position,
                UserStep.position < old_position
            ).update({"position": UserStep.position + 1}, synchronize_session=False)
        elif new_position > old_position:
            # Moving forward: Decrement positions of items between old and new positions
            session.query(UserStep).filter(
                UserStep.position <= new_position,
                UserStep.position > old_position
            ).update({"position": UserStep.position - 1}, synchronize_session=False)

        # Update the position of the moved item
        user_step.position = new_position
        session.commit()

    session.close()
