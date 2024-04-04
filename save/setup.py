import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("app.py", base=base, icon="icon.ico")
]

setup(
    name="OGAutomatic",
    version="1.0.0",
    description="This is an application to save time in combining documents for OG.",
    executables=executables
)
