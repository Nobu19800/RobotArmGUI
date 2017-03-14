echo off
cd /d %~dp0
setlocal
for %%I in (python.exe) do if exist %%~$path:I set f=%%~$path:I
if exist %f% do (
  %f:python.exe=%omniidl.exe -bpython -I"%RTM_ROOT%rtm\idl" -I"C:\IDL" -I"C:\UserDefType" idl/ManipulatorCommonInterface_Common.idl idl/ManipulatorCommonInterface_MiddleLevel.idl idl/ManipulatorCommonInterface_DataTypes.idl 
) else do (
  echo "python.exe" can not be found.
  echo Please modify PATH environmental variable for python command.
)
endlocal
