@ECHO OFF

REM ############################################
REM #
REM # BB simulator will be launched
REM #
REM ############################################

start %RIM_HOME%\%DEVICE_OS%\simulator\fledge.exe /app=%RIM_HOME%\%DEVICE_OS%\simulator\Jvm.dll /session=%DEVICE% /app-param=DisableRegistration /app-param=JvmAlxConfigFile:%DEVICE%.xml /no-save-settings /comm-cable-connected /no-secure /no-sdcard-inserted /no-show-plastics /pin=%PIN% /ignore-data-port-conflicts /app-param=IPPPSourcePort:%PORT% %HANDHELD% %LCD%

