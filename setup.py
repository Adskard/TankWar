import cx_Freeze
executables=[cx_Freeze.Executable("TankWar1.py")]
cx_Freeze.setup(
name="TankWar1",
options={"build_exe":{"packages":["pygame"],"include_files":["boom.png","tank.gif","terrain.gif","firmament.gif","tank1.gif","tank2.gif","projectile1.png"]}},
executables=executables
)