from kivy.uix.screenmanager import FadeTransition, ScreenManager, SlideTransition

screen_history = []


def get_screen_by_name(manager, screen_name):
    return manager.get_screen(screen_name)


def go_back(screen_manager, transition=FadeTransition()):
    if screen_history:
        previous_screen = screen_history.pop()
        screen_manager.transition = transition
        screen_manager.current = previous_screen


def navigate_to_screen(screen_manager, screen_name, transition=SlideTransition()):
    if screen_manager.current:
        screen_history.append(screen_manager.current)
    screen_manager.transition = transition
    screen_manager.current = screen_name
