from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('tkedit.py', base=base)
]

setup(name='tkedit',
      version = '1.0',
      description = 'A tkinter text editor',
      options = dict(build_exe = buildOptions),
      executables = executables)
