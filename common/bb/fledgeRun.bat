@ECHO OFF
REM ############################################
REM #
REM # BB simulator will be run with %1 argument
REM #
REM ############################################

call %RIM_HOME%\%DEVICE_OS%\simulator\fledgecontroller.exe /session=%DEVICE% <%1
