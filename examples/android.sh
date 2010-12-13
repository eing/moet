#!/bin/sh
################################################
#
# This file contains environment variables that 
# should be configured to your environment.
#
################################################

# Test framework settings
export LOG_LEVEL=DEBUG

# Device settings
export DEVICE=android
export MOBILE_DEVICE=android
export DEVICE_OS=2.8
export HOST=localhost
export PORT=5554
export DEVICE_RESOLUTION=320x480
export FULL_DEVICE=$DEVICE-$DEVICE_OS

# These are global test variables
# Note. Install in non-spaced directory e.g. NOT Program Files/
export TEST_ROOT=c:/moet
export PYTHON_TEST_ROOT=/cygdrive/c/moet
export PYTHONPATH="$PYTHON_TEST_ROOT/common:$PYTHON_TEST_ROOT/examples"
export RUN_OPTION=TEST

# Create test output directory if it does not exist
export folder=`date +%m%d20%y-%s`

if [ ! -e $TEST_ROOT/results ]
then
  mkdir $TEST_ROOT/results
fi 

export TEST_OUTPUT=$TEST_ROOT/results/$FULL_DEVICE-$folder
if [ ! -e $TEST_OUTPUT ]
then
  mkdir $TEST_OUTPUT
fi
