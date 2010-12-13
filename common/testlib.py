#
# Copyright 2010 Intuit, Inc.
#
# Licensed under the Eclipse Public License, Version 1.0 (the "License"); you may
# not use this file except in compliance with the License. Please see the License 
# for the specific language governing permissions and limitations.
# You may obtain a copy of the License at
#
# http://www.eclipse.org/legal/epl-v10.html
#

""" 
    Common test library for all devices.
"""

import os
import logger

log = logger.getLogger('testlib')

class TestException(Exception):
    """ Application base class for test exceptions """
    def __init__(self, ErrorMsg):
        self.ErrorMsg = ErrorMsg

    def __repr__(self):
        return repr('[' + self.ErrorCode + '] ' + self.ErrorMsg)
         
    def getErrorMessage(self):
        return self.ErrorMsg

    def getErrorCode(self):
        return self.ErrorCode


# Setup and Envirnoment Exceptions
class SetupException(TestException): ErrorCode = 100
class EnvironmentException(TestException): ErrorCode = 150
class OSSystemException(TestException): ErrorCode = 151
class TestITException(TestException) : ErrorCode = 160

# Test Execution Exceptions
class TestExecutionException(TestException): ErrorCode = 200
class TestDataException(TestException): ErrorCode = 201
class BatchToolException(TestException): ErrorCode = 301
class BatchRunException(TestException): ErrorCode = 302

# Test Verification Exceptions
class TestVerificationException(TestException): ErrorCode = 400
class ImageVerificationException(TestException): ErrorCode = 402
class MissingImageFileException(TestException): ErrorCode = 403

class testEnv:
    """ Reads in environment variables used in Test Framework """

    runOptionList = ('CAPTURE', 'TEST')

    def __init__(self):
        self.device = os.getenv('DEVICE')
        self.deviceOS = os.getenv('DEVICE_OS')
        self.devicePin = os.getenv('DEVICE_PIN')
        self.devicePort = os.getenv('DEVICE_PORT')
        self.rimHome = os.getenv('RIM_HOME')
        self.version = os.getenv('Version')
        self.imageTool = os.getenv('IMAGE_TOOL')
        self.mobileEnv= os.getenv('MOBILE_ENV')
        self.mobileDevice = os.getenv('MOBILE_DEVICE').lower()
        self.testroot = os.getenv('TEST_ROOT')
        self.runOption = os.getenv('RUN_OPTION')
        self.resources = self.testroot + '/resources/' + self.mobileDevice + '/'

        self.fullDevice = self.device + '-' + self.deviceOS
        self.testoutput = os.getenv('TEST_OUTPUT')
        # set resolution is done by device implementation
        self.resX = ''
        self.resY = ''
        self.res = ''

    def getDevice(self):
        return self.device

    def setDevice(self, device):
        self.device = device

    def setDeviceOS(self, deviceOS):
        self.deviceOS = deviceOS

    def getResolution(self):
        return self.res

    def getFullDevice(self):
        return self.fullDevice

    def getImageTool(self):
        return self.imageTool

    def getMobileEnv(self):
        return self.mobileEnv

    def setMobileEnv(self, mobileEnv):
        self.mobileEnv = mobileEnv

    def getRunOption(self):
        if isinstance(self.runOption, str) == False or self.runOption == '':
           self.runOption = self.runOptionList[1] 
        return self.runOption.upper()

    def setRunOption(self, runOption):
        if isinstance(runOption, str) == False or self.runOption == '':
           self.runOption = self.runOptionList[1] 
        self.runOption = runOption

    def getMobileDevice(self):
        return self.mobileDevice

    def getSimulatorHome(self):
        return self.simulatorHome

    def getTestRoot(self):
        return self.testroot

    def getTestOutput(self):
        return self.testoutput

    def getDeviceClass(self):
        """ Returns the device to test """
        mobileDevice = self.getMobileDevice()

        if mobileDevice == 'android':
            import android 
            deviceClass = android.AndroidImpl()
        elif mobileDevice == 'iphone':
            import iphone 
            deviceClass = iphone.iPhoneImpl()
        elif mobileDevice == 'pearl':
            import pearl 
            deviceClass = pearl.PearlImpl()
        elif mobileDevice == 'storm':
            import storm
            deviceClass = storm.StormImpl()
        else:
            import bb
            deviceClass = bb.BlackBerryImpl()
        log.debug('Device is ' + mobileDevice)
        return deviceClass

    def updateEnv(self, variable, value):
        """ Update existing environment variable with value """

        log.debug('Updating ' + variable + ' to ' + value);
        keys = os.environ.keys()
        from re import search
        for key in keys:
            if not search(variable, key):
                os.environ[variable]=value
        

""" Create an instance of testenv """
testenv = testEnv()

if __name__ == '__main__':
    print testenv.getDeviceClass()
