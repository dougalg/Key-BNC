import sys, os
from cx_Freeze import setup, Executable

data_dirs = ['KEY_BNC', 'Data']

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
	"packages": ["os"],
	"excludes": ['tk', '_tkagg', '_gtkagg', '_gtk', 'tcl'],
	"include_files": [os.path.join(data_dirs[0], data_dirs[1])]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(
	name = "KEY_BNC",
	version = "1.3",
	description = "Key BNC",
	options = {"build_exe": build_exe_options},
	executables = [Executable("KEY_BNC_app.py", base=base)]
)
