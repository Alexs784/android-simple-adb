from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from commands.name_constants import COMMAND_TAP_ON_VIEW_BY_ID_NAME, COMMAND_SLEEP_NAME, COMMAND_CLEAR_APP_DATA_NAME, \
    COMMAND_LAUNCH_APP_NAME, COMMAND_PRESS_BACK_NAME, COMMAND_INPUT_TEXT_ON_KEYBOARD_NAME, \
    COMMAND_PRESS_ENTER_ON_KEYBOARD_NAME, COMMAND_TAKE_SCREENSHOT_NAME
from commands.placeholder_constants import DEVICE_SERIAL_NUMBER_PLACEHOLDER, PARAMETER_PLACEHOLDER
from storage import Base
from storage.database.model.command import Command
from storage.database.model.step import Step, get_step

Session = sessionmaker()


def init_database():
    engine = create_engine("sqlite:///android_automation.db")
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


def get_session():
    return Session()


@event.listens_for(Step.__table__, 'after_create')
def populate_database_with_preloaded_data(*args, **kwargs):
    print("Populating database after first creation")
    session = get_session()
    session.add_all(get_supported_steps())
    session.commit()
    session.close()


def get_supported_steps():
    return [
        get_step(
            name=COMMAND_LAUNCH_APP_NAME,
            commands=[
                Command(
                    device_serial_number_command() + " shell am start -n "
                    + PARAMETER_PLACEHOLDER + "1/" + PARAMETER_PLACEHOLDER + "2",
                    True
                )
            ],
            parameters_names=["Application id", "Activity name"],
            parameters_descriptions={"Activity name": "Fully qualified activity name, including its package"}
        ),
        get_step(
            name=COMMAND_CLEAR_APP_DATA_NAME,
            commands=[Command(device_serial_number_command() + " shell pm clear " + PARAMETER_PLACEHOLDER + "1",
                              True)],
            parameters_names=["Application id"],
            parameters_descriptions={""}
        ),
        get_step(
            name=COMMAND_SLEEP_NAME,
            commands=[Command(" sleep " + PARAMETER_PLACEHOLDER + "1", False)],
            parameters_names=["Time in seconds"],
            parameters_descriptions={
                "Time in seconds": "The time in seconds the script is going to wait before executing the next step"
            }
        ),
        get_step(
            name=COMMAND_TAP_ON_VIEW_BY_ID_NAME,
            commands=[
                Command(device_serial_number_command() + " shell uiautomator dump", True),
                Command(device_serial_number_command() + " pull /sdcard/window_dump.xml ./", True),
                Command(
                    """shell input tap $(perl -ne 'printf "%d %d", ($1+$3)/2, ($2+$4)/2 if /resource-id=\""""
                    + PARAMETER_PLACEHOLDER + "1:id\/" + PARAMETER_PLACEHOLDER
                    + """2"[^>]*bounds="\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]"/' ./window_dump.xml)""",
                    True
                )
            ],
            parameters_names=["Application id", "View id"],
            parameters_descriptions={"View id": "The id of the view to tap on"}
        ),
        get_step(
            name=COMMAND_PRESS_BACK_NAME,
            commands=[Command(device_serial_number_command() + " shell input keyevent 4", True)],
            parameters_names=[],
            parameters_descriptions={}
        ),
        get_step(
            name=COMMAND_INPUT_TEXT_ON_KEYBOARD_NAME,
            commands=[
                Command(device_serial_number_command() + " shell input text " + PARAMETER_PLACEHOLDER + "1", True)
            ],
            parameters_names=["Text"],
            parameters_descriptions={"Text": "Text to input on the keyboard (assuming the keyboard is already open)"}
        ),
        get_step(
            name=COMMAND_PRESS_ENTER_ON_KEYBOARD_NAME,
            commands=[Command(device_serial_number_command() + " shell input keyevent 66", True)],
            parameters_names=[],
            parameters_descriptions={}
        ),
        get_step(
            name=COMMAND_TAKE_SCREENSHOT_NAME,
            commands=[
                Command(device_serial_number_command() + " shell screencap -p /sdcard/screenshot.png", True),
                Command(
                    device_serial_number_command() + " pull /sdcard/screenshot.png " + PARAMETER_PLACEHOLDER + "1", True
                )
            ],
            parameters_names=["Destination folder"],
            parameters_descriptions={
                "Destination folder": "The folder where the screenshot is going to be saved. Must be an already existing folder on your machine "
            }
        )
    ]


def device_serial_number_command():
    return "-s " + DEVICE_SERIAL_NUMBER_PLACEHOLDER
