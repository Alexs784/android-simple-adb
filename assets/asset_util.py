import os
import sys

image_buttons_width = .11
image_buttons_height = .11
positive_button_background = (0.38, 1.70, 0.38, 1)
negative_button_background = (2.13, 0.05, 0.05, 1)
buttons_bottom_alignment_value = .08

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
