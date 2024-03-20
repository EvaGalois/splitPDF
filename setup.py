import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base, icon="icon.ico")]  # 将"your_script.py"替换为你的Python脚本文件名

build_options = {
    "packages": ["PyPDF2", "PyQt5.QtWidgets", "PyQt5.QtGui"],
    "include_files": ["icon.ico"],  # 如果你的程序用到了图标文件，将其包含在这里
    "excludes": [],
}

setup(
    name="PDF Splitter",
    version="1.0",
    description="PDF拆分合并工具",
    options={"build_exe": build_options},
    executables=executables
)