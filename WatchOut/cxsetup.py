from cx_Freeze import setup, Executable

setup(
    name = "run.py" ,
    version = "Beta 1.4" ,
    description = "Watch Out!" ,
    executables = [Executable("run.py")] ,
)
