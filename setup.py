from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine-tuning.
build_options = {
    'packages': ['kivy', 'sqlalchemy'],
    'excludes': [],
    "silent": True
}

include_files = ['assets']

if sys.platform == 'win32':
    base = 'Win32GUI'
else:
    base = None

executables = [
    Executable('main.py', base=base, target_name='SimpleAdb')
]

setup(
    name='SimpleAdb',
    version='0.0.6',
    description='',
    options={
        'build_exe': build_options,
    },
    executables=executables,
)
