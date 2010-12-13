@ECHO OFF

REM ############################################
REM #
REM # This takes a screenshot from BB simulator.
REM #
REM ############################################

if ""%1""=="""" (
     set outfile=./pic%folder%.png
) else (
     set outfile=%1.png
)

set JAVALOADER_HOME=%RIM_HOME%\%DEVICE_OS%\bin

set BACKUP_PATH=%PATH%
set PATH=%JAVALOADER_HOME%;%PATH%

call JavaLoader.exe -p%DEVICE_PORT% -p%DEVICE_PIN% -q -u screenshot %outfile%
mv %outfile% %TEST_OUTPUT%\%outfile%

set PATH=%BACKUP_PATH%
