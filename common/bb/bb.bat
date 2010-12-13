REM ######################################################
REM #
REM # This file is only created for convenience 
REM # to execute the batch tools in this folder.
REM #
REM ######################################################

REM  Test framework settings
set MOBILE_DEVICE=bb
set LOG_LEVEL=INFO
set IMAGE_TOOL=c:\mobilei\install\ImageMagick-6.5.9-Q8
set CYGWIN_HOME=c:\cygwin
set JAVA_HOME=c:\mobile\install\jre6
set PATH=%CYGWIN_HOME%\bin;%IMAGE_TOOL%;%JAVA_HOME%\bin;%PATH%

REM  Device settings
set DEVICE=8300
set DEVICE_OS=4.5.0
set DEVICE_RESOLUTION=320x240

REM  Application settings
set Version=1.0

REM  Global test variables
REM  Install in non-spaced directory i.e. NOT Program Files\
set RIM_HOME=c:\mobile\install\RIM\%DEVICE_OS%
set PYTHON_TEST_ROOT=\cygdrive\c\mobile
set PYTHONPATH=%PYTHON_TEST_ROOT%\common;%PYTHON_TEST_ROOT%\tests
set TEST_ROOT=c:\mobile
set nodosfilewarning=true

REM  Create test output directory if it does not exist
set folder=`date +%m%d20%y-%s`

if not exist %TEST_ROOT%\results (
  mkdir %TEST_ROOT%\results
)

set FULL_DEVICE=%DEVICE%-%DEVICE_OS%
set TEST_OUTPUT=%TEST_ROOT%\results\%FULL_DEVICE%-%folder%
if not exist %TEST_OUTPUT (
  mkdir %TEST_OUTPUT%
)
