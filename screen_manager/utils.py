from kivy.uix.screenmanager import FadeTransition, ScreenManager


def get_screen_by_name(manager, screen_name):
    for screen in manager.screens:
        if screen.name == screen_name:
            return screen
    return None


def remove_screen(manager, screen, transition=FadeTransition()):
    manager.transition = transition
    manager.current = manager.previous()
    manager.remove_widget(screen)
