@ECHO OFF

REM ############################################
REM #
REM # This installs YourAPP to BB simulator.
REM #
REM ############################################


set JAVALOADER_HOME=%RIM_HOME%\%DEVICE_OS%\bin

set oldPATH=%PATH%

set PATH=%JAVALOADER_HOME%;%PATH%
pushd %JAVALOADER_HOME%

REM Replace YourAPP with your product name
call JavaLoader.exe -p%DEVICE_PORT% -p%DEVICE_PIN% -q -u load YourAPP%DEVICE_BUILD%_%Version%.jad

REM Replace YourAPP with your product name
rem del %JAVALOADER_HOME%\YourAPP*.jar
rem del %JAVALOADER_HOME%\YourAPP*.jad
rem del %JAVALOADER_HOME%\YourAPP*.cod

set PATH=%oldPATH%
popd
