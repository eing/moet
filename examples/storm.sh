#!/bin/sh
################################################
#
# This file contains environment variables that 
# should be configured to your environment.
#
################################################

# Test framework settings
export MOBILE_DEVICE=storm
export LOG_LEVEL=INFO
export IMAGE_TOOL="c:/mobile/install/ImageMagick-6.5.9-Q8"
export CYGWIN_HOME=c:/cygwin
export JAVA_HOME=c:/root/sdk/java
export PATH=".:$CYGWIN_HOME/bin:$IMAGE_TOOL:$JAVA_HOME/bin:$PATH"

# Device settings
export DEVICE=9550
export DEVICE_OS=5.0.0
export DEVICE_PORT=25601
export DEVICE_PIN=553648139

export RIM_HOME="c:/mobile/install/bb"
export TEST_ROOT=c:/moet
export PYTHON_TEST_ROOT=/cygdrive/c/moet
export PYTHONPATH="$PYTHON_TEST_ROOT/common:$PYTHON_TEST_ROOT/examples"
export PYTHONSTARTUP=$PYTHON_TEST_ROOT/examples/stormstartup.py
export RUN_OPTION=TEST
export nodosfilewarning=true


# Create test output directory if it does not exist
export FULL_DEVICE=$DEVICE-$DEVICE_OS
export folder=`date +%m%d20%y-%s`
export folder=1

if [ ! -e $TEST_ROOT/results ]
then
  mkdir $TEST_ROOT/results
fi 

export TEST_OUTPUT=$TEST_ROOT/results/$FULL_DEVICE-$folder
if [ ! -e $TEST_OUTPUT ]
then
  mkdir $TEST_OUTPUT
fi
