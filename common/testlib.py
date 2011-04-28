#
# Copyright 2010 Intuit, Inc.
#
# Licensed under the Eclipse Public License, Version 1.0 (the "License"); 
# you may not use this file except in compliance with the License. Please 
# see the License for the specific language governing permissions and 
# limitations. You may obtain a copy of the License at
#
# http://www.eclipse.org/legal/epl-v10.html
#

""" 
    Common test library for all devices.
"""

__version__ = '1.0'
__license__ = "EPL 1"
__author__ = [ 'Eing Ong @eingong' ]

import os

class testEnv:
    """ Reads in environment variables used in tests. 
        Examples:
        MOET - /Users/<name>/moet
        MOET_DEVICE - bb8130/bb9550/android/iphone
        MOET_OS - 5.0.0/2.2/4.2
        MOET_RESOLUTION - 240x320/320x480/480x800
        MOET_RESULTS - $MOET/results
        MOET_MODE - CAPTURE/TEST/DEMO
        IMAGE_TOOL (if not in system PATH)
    """

    runOptionList = ('CAPTURE', 'TEST', 'DEMO')

    def __init__(self):
        self.devicePin = os.getenv('DEVICE_PIN')
        self.devicePort = os.getenv('DEVICE_PORT')
        self.rimHome = os.getenv('RIM_HOME')
        self.version = os.getenv('Version')
        self.imageTool = os.getenv('IMAGE_TOOL')
        self.testroot = os.getenv('MOET')
        if not self.testroot is None:
            self.resources = os.path.join(self.testroot, 'resources')
        self.mobileDevice = os.getenv('MOET_DEVICE')
        if not self.mobileDevice is None:
            self.fullDevice = self.mobileDevice
            self.mobileDevice = self.mobileDevice.lower()
            self.resources = os.path.join(self.resources, self.mobileDevice)
        self.deviceOS = os.getenv('MOET_OS')
        if not self.deviceOS is None:
            self.fullDevice = self.fullDevice + '-' + self.deviceOS 
        self.runOption = os.getenv('MOET_MODE')
        self.orientation = os.getenv('ORIENTATION')
        self.testoutput = os.getenv('MOET_RESULTS')
        self.res = os.getenv('MOET_RESOLUTION')
        if not self.res is None:
            self.resX = self.res.split('x')[0]
            self.resY = self.res.split('x')[1]
        if not self.res is None:
            self.resources = os.path.join(self.resources, self.res)

    def setDeviceOS(self, deviceOS):
        self.deviceOS = deviceOS

    def getResolution(self):
        return self.res

    def getFullDevice(self):
        return self.fullDevice

    def getImageTool(self):
        return self.imageTool

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
        return deviceClass

    def updateEnv(self, variable, value):
        """ Update existing environment variable with value """

        keys = os.environ.keys()
        from re import search
        for key in keys:
            if not search(variable, key):
                os.environ[variable]=value
        

""" Create an instance of settings """
settings = testEnv()
