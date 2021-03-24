from datetime import datetime

from storage.database.database_manager import get_session
from storage.database.model.user_script import UserScript


def get_scripts():
    session = get_session()
    scripts = session.query(UserScript).order_by(UserScript.id.desc()).all()
    session.close()
    return scripts


def create_script_in_database():
    current_date_time = datetime.now()
    script_name = current_date_time.strftime("%d-%m-%Y %H:%M")
    script = UserScript(name=script_name)
    session = get_session()
    session.add(script)
    session.commit()
    session.refresh(script)
    session.close()
    return script


def update_script_name(script_id, script_name):
    session = get_session()
    script = session.query(UserScript).filter_by(id=script_id).first()
    script.name = script_name
    session.commit()
    session.close()


def delete_script(script_id):
    session = get_session()
    session.query(UserScript).filter(UserScript.id == script_id).delete()
    session.commit()
    session.close()
