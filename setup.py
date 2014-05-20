import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],
                     "excludes": ['tk', '_tkagg', '_gtkagg', '_gtk', 'tcl'],
                     "include_files": [r'LL_OR_BNC\Data']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "LL_OR_BNC",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("LL_OR_BNC.py", base=base)])
