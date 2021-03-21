from screen_manager.screen_manager import ScreenManagerApp
from storage.database import database_manager


def main():
    database_manager.init_database()
    ScreenManagerApp().run()


if __name__ == '__main__':
    main()
