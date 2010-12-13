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
    Library containing all BlackBerry device common functions. 
"""

import os
import testlib
import logger
import time

log = logger.getLogger('bblib')
testoutput = testlib.testenv.testoutput
batchroot = testlib.testenv.testroot + '/common/bb/'
device = testlib.testenv.getDevice()
deviceOS = testlib.testenv.deviceOS

def setDeviceResolution():
    """ Sets device resolution """
    if device.startswith('95'):
        testlib.testenv.res = '480x360'
        testlib.testenv.resX = '480'
        testlib.testenv.resY = '360'
    elif device.startswith('81'):
        testlib.testenv.res = '240x260'
        testlib.testenv.resX = '240'
        testlib.testenv.resY = '260'
    elif device.startswith('9') or device.startswith('89'):
        testlib.testenv.res = '480x320'
        testlib.testenv.resX = '480'
        testlib.testenv.resY = '320'
    else:
        testlib.testenv.res = '320x240'
        testlib.testenv.resX = '320'
        testlib.testenv.resY = '240'


class bbEnv:
    """ This is specific to BlackBerry Environment"""


    def __init__(self):
        self.pin = int(testlib.testenv.devicePin)
        self.port = int(testlib.testenv.devicePort)
        self.build = None
        setDeviceResolution()
    
    def setPort(self, port):
        """ Sets port """
        self.port = int(port)

    def getPort(self):
        """ Returns port as a string """
        return str(self.port)

    def setPin(self, pin):
        """ Sets pin"""
        self.pin = int(pin)

    def getPin(self):
        """ Returns pin as a string """
        return hex(self.pin)

    def incrPin(self):
        """ Increases pin by 1 """
        self.pin = self.pin + 1

    def incrPort(self):
        """ Increases pin by 1 """
        self.port = self.port + 1

    def getDeviceBuild(self):
        """ 
            Resets device build.
            @returns 8300 if device is of 320x240 or 83xx, 88xx, 85xx
                     8900 if device is of 480x320 or 89xx, 9xxx
        """
        if self.build is None:
            self.setDeviceBuild()
        return self.build

    def setDeviceBuild(self):
        """ Resets device build. """
        if device.startswith('9') or device.startswith('89'):
            self.build = '8900'
        else:
            self.build = '8300'



bbenv = bbEnv()


def backspaces(count=1, execute=True):
    """ 
        Press backspaces specified by count. 
        If execute, run in simulator, otherwise return string.
    """
    if not isinstance(count, int):
        return

    log.debug('Entering %d backspaces' % count)
    if execute:
        outfilepath = testoutput + '/backspaces.fct'
        outfile = open(outfilepath, 'w+')
        while count > 0:
            outfile.write('KeyPress(BACKSPACE)\n')
            outfile.write('KeyRelease(BACKSPACE)\n')
            if count % 15 == 0:
                outfile.write('Pause(1)\n')
            count = count - 1
        outfile.write('Pause(1)\n')
        outfile.close() 
        fledgeRun(outfilepath)
    else:
        deviceStr = ''
        while count > 0:
            deviceStr = deviceStr + 'KeyPress(BACKSPACE)\n' \
                + 'KeyRelease(BACKSPACE)\n'
            if count % 15 == 0:
                deviceStr = deviceStr + 'Pause(1)\n'
            count = count - 1
        return deviceStr + pause(1, False)

def thumbwheel(direction='up', count=1, execute=True):
    """  
        Enter thumbwheelrolls specified by count and direction. 
        If execute, run in simulator, otherwise return string.
    """

    log.debug('Entering %d %s thumbwheelrolls' % (count, direction))
    deviceStr = ''
    if direction == 'up':
        direction = '-1'
    else:
        direction = '1'
    outfilepath =  testoutput + '/scrolls.fct'
    outfile = open(outfilepath, 'w+')
    while count > 0:
        scroll = 'ThumbWheelRoll(' + direction + ')\nPause(1)\n'
        deviceStr = deviceStr + scroll
        outfile.write(scroll)
        count = count - 1
    outfile.close() 
    if execute:
        fledgeRun(outfilepath)
    else:
        return deviceStr

def trackball(direction='left', count=1, execute=True):
    """ 
        Enter trackball rolls specified by count and direction.
        If execute, run in simulator, otherwise return string.
    """

    log.debug('Entering %d %s trackballrolls' % (count, direction))
    deviceStr = ''
    directionX = '0' 
    directionY = '0' 
    if direction == 'up':
        directionY = '10'
    elif direction == 'down':
        directionY = '-10'
    elif direction == 'left':
        directionX= '-10'
    else:
        directionX= '10'
    outfilepath = testoutput + '/rolls.fct'
    outfile = open(outfilepath, 'w+')
    while count > 0:
        roll = 'TrackBallRoll(' + directionX + ',' + directionY + ')\n' \
            + 'Pause(1)\n'
        deviceStr = deviceStr + roll
        outfile.write(roll)
        count = count - 1
    outfile.close() 
    if execute:
        fledgeRun(outfilepath)
    else:
        return deviceStr


def simulateDeviceKey(char):
    """ Generate device key in simulator """
    if char.isdigit():
        deviceStr = 'KeyPress(ALT)\n'
        if char == '0':
            deviceStr = deviceStr + 'KeyPress(_0)\nKeyRelease(_0)\n'
        elif char == '1': 
            deviceStr = deviceStr + 'KeyPress(W)\nKeyRelease(W)\n'
        elif char == '2':    
            deviceStr = deviceStr + 'KeyPress(E)\nKeyRelease(E)\n'
        elif char == '3':    
            deviceStr = deviceStr + 'KeyPress(R)\nKeyRelease(R)\n'
        elif char == '4':    
            deviceStr = deviceStr + 'KeyPress(S)\nKeyRelease(S)\n'
        elif char == '5':    
            deviceStr = deviceStr + 'KeyPress(D)\nKeyRelease(D)\n'
        elif char == '6':    
            deviceStr = deviceStr + 'KeyPress(F)\nKeyRelease(F)\n'
        elif char == '7':    
            deviceStr = deviceStr + 'KeyPress(Z)\nKeyRelease(Z)\n'
        elif char == '8':    
            deviceStr = deviceStr + 'KeyPress(X)\nKeyRelease(X)\n'
        elif char == '9':    
            deviceStr = deviceStr + 'KeyPress(C)\nKeyRelease(C)\n'
        deviceStr = deviceStr + 'KeyRelease(ALT)\n'
    elif char.isspace():
        deviceStr = 'KeyPress(SPACE)\nKeyRelease(SPACE)\n'
    elif char == '_':
        deviceStr = 'KeyPress(ALT)\nKeyPress(U)\nKeyRelease(U)\n' \
            + 'KeyRelease(ALT)\n'
    elif char == '@':
        deviceStr = 'KeyPress(ALT)\nKeyPress(P)\nKeyRelease(P)\n' \
            + 'KeyRelease(ALT)\n'
    elif char == '.':
        deviceStr = 'KeyPress(ALT)\nKeyPress(M)\nKeyRelease(M)\n' \
            + 'KeyRelease(ALT)\n'
    elif char == ':':
        deviceStr = 'KeyPress(ALT)\nKeyPress(H)\nKeyRelease(H)\n' \
            + 'KeyRelease(ALT)\n'
    elif char.isupper():
        deviceStr = '\nKeyPress(LEFT_SHIFT)\n' + 'KeyPress(' + char + ')\n'  \
            + 'KeyRelease(' + char + ')\nKeyRelease(LEFT_SHIFT)\nPause(1)\n'
    elif char.islower():
        deviceStr = 'KeyPress(' + char + ')\n' + 'KeyRelease(' + char + ')\n'
    else:
        raise testlib.TestDataException('Unsupported character to enter - ' + char)
    return deviceStr

def enterString(string, execute=True):
    """ 
        Press keystrokes for String in simulator.
        If execute, run in simulator, otherwise return string.
    """
    if string is None:
        return ''
    strlen = len(string)
    if strlen <= 0:
        return ''
    index = 0 
    deviceStr = ''
    outfilepath = testoutput + '/string.fct'
    outfile = open(outfilepath, 'w+')

    deviceOS = testlib.testenv.deviceOS
    device = testlib.testenv.device
    if not deviceOS.startswith('4.2') and not device.startswith('83'):
        deviceStr = 'StringInjection(' + string + ')\nPause(1)\n' 
        if execute:
            fledgeRun(deviceStr, False)
            return
        else:
            return deviceStr

    while index < strlen:
        deviceChar = simulateDeviceKey(string[index]) 
        deviceStr = deviceStr + deviceChar 
        outfile.write(deviceChar)
        if deviceOS.startswith('4.6') or deviceOS.startswith('4.7'):
            outfile.write(pause(1, False))
            deviceStr = deviceStr + pause(1,False)
        index = index + 1
        if (index % 30 == 0) and (execute is True):
            outfile.close()
            fledgeRun(outfilepath)
            outfile = open(outfilepath, 'w+')
            outfile.truncate(0)
    outfile.write(pause(1, False))
    outfile.close()
    if execute:
        fledgeRun(outfilepath)
    else:
        return deviceStr

def enter(string=None, execute=True):
    """ 
        Press Enter key in simulator.
        If execute, run in simulator, otherwise return string.
    """
    if not string is None:
        return enterString(string, execute)
    entercmd = 'KeyPress(ENTER)\nKeyRelease(ENTER)\nPause(1)\n'
    if execute:
        fledgeRun(entercmd, False)
    else:
        return entercmd

def escape(execute=True):
    """ 
        Press Escape key in simulator.
        If execute, run in simulator, otherwise return string.
    """
    escapeString = 'KeyPress(ESCAPE)\nKeyRelease(ESCAPE)\nPause(1)\n'
    if execute:
        fledgeRun(escapeString, False)
    else:
        return escapeString

def menu(execute=True):
    """ 
        Press Menu key in simulator.
        If execute, run in simulator, otherwise return string.
    """
    menuString = 'KeyPress(Front_Convenience)\nKeyRelease(Front_Convenience)\nPause(1)\n'
    if execute:
        fledgeRun(menuString, False)
    else:
        return menuString

def pause(seconds=1, execute=True):
    """ 
        Pause simulator specified by seconds.
        If execute, run pause in simulator, otherwise return string.
    """
    pauseString = 'Pause(%d)\n' % seconds
    if execute:
       fledgeRun(pauseString, False)
    else:
        return pauseString


def mdsStart():
    """ Start Mobile Data Service, required for internet connectivity """
    log.debug('Starting MDS')
    os.system('pushd ' + testlib.testenv.rimHome + '/' \
        + testlib.testenv.deviceOS + '/MDS; cmd /C run.bat')
    time.sleep(5)
    result = os.popen('ps -aW|grep java').readline()
    log.info('MDS: ' + result)
    if not(result):
        raise testlib.SetupException('MDS start failed')
    else:
        return True


def fledgeStart(deviceVal=device, deviceOSVal=deviceOS):
    """ Start blackBerry simulator """
    log.info('Starting Fledge')
    if deviceVal <> device : 
        bbenv.incrPort()
        bbenv.incrPin()

    fledgeTemplate = batchroot + '/fledgeStart.bat'
    fledgeRunTemplate = batchroot + '/fledgeRun.bat'
    screenshotTemplate = batchroot + '/getScreenShot.bat'
    fledgeStart = testoutput + '/fledge' + deviceVal + '.bat'
    fledgeRun = testoutput + '/fledgeRun' + deviceVal + '.bat'
    screenshotRun = testoutput + '/getScreenShot' + deviceVal + '.bat'
    testoutputDos = testoutput.replace('/','\\\\')
    rimHomeUnix = testlib.testenv.rimHome
    rimHomeDos = rimHomeUnix.replace('/','\\\\')

    keepLcdOn = ' '
    if deviceOSVal.startswith('4.5'):
        # add /keep-lcd-on
        keepLcdOn = '\/keep-lcd-on' 

    handheld = ' '
    if not deviceOSVal.startswith('4.7'):
        # remove /handheld=device
        handheld = '\/handheld=' + deviceVal

    # create fledgeStart<device>.bat
    cmd = 'cat ' + fledgeTemplate + "| sed 's/%DEVICE%/" + deviceVal \
        + '/g;s/%DEVICE_OS%/' + deviceOSVal + '/g;s/%PORT%/' + bbenv.getPort() \
        + '/g;s/%LCD%/' + keepLcdOn \
        + '/g;s/%HANDHELD%/' + handheld  \
        + '/g;s/%PIN%/' + bbenv.getPin() + "/g' >" + fledgeStart
    os.system(cmd)

    # create getScreenShot<device>.bat
    os.system('cat ' + screenshotTemplate + "| sed 's/%RIM_HOME%/" + rimHomeDos \
        + '/g;s/%DEVICE_PORT%/' + bbenv.getPort() \
        + '/g;s/%DEVICE_PIN%/' + bbenv.getPin() \
        + '/g;s/%TEST_OUTPUT%/' + testoutputDos \
        + '/g;s/%DEVICE_OS%/' + deviceOSVal  + "/g' >" + screenshotRun)
    
    # create fledgeRun<device>.bat
    cmd = 'cat ' + fledgeRunTemplate + "| sed 's/%DEVICE%/" + deviceVal \
        + '/g;s/%DEVICE_OS%/' + deviceOSVal + "/g' >" + fledgeRun
    os.system(cmd)

    # Start simulator
    os.system('pushd ' + testoutput + '; cmd /C ' + fledgeStart)

    # Verify simulator starts successfully
    result = os.popen('ps -aW|grep fledge').readline()
    log.info('Fledge: ' + result)
    if not(result):
        raise testlib.SetupException('Fledge start failed')
    else:
        time.sleep(15)
    return True


def javaloaderStart():
    """
        JavaLoader is used for installing application and taking screenshots
    """
    testroot = testlib.testenv.testroot
    version = testlib.testenv.version
    deviceBuild = bbenv.getDeviceBuild()
    rimHomeUnix = testlib.testenv.rimHome
    devicePort =  testlib.testenv.devicePort
    devicePin =  testlib.testenv.devicePin
    

    loaderTemplate = batchroot + '/javaloaderStart.bat'
    loaderStart = testoutput + '/javaloaderStart' + device + '.bat'
    rimHomeDos = rimHomeUnix.replace('/','\\\\')

    os.system('cat ' + loaderTemplate + "| sed 's/%RIM_HOME%/" + rimHomeDos \
        + '/g;s/%Version%/' + testlib.testenv.version \
        + '/g;s/%DEVICE_BUILD%/' + deviceBuild \
        + '/g;s/%DEVICE_PORT%/' + devicePort \
        + '/g;s/%DEVICE_PIN%/' + bbenv.getPin() \
        + '/g;s/%DEVICE_OS%/' + deviceOS  + "/g' >" + loaderStart)

    cmd = 'cmd /C cp ' + testroot + '/install/' + version + '/' \
        + deviceBuild + '/* ' + testlib.testenv.rimHome + '/' + deviceOS + '/bin'
    os.system(cmd)
    cmd = 'pushd ' + testoutput + '; cmd /C javaloaderStart' + device + '.bat'
    os.system(cmd)

def fledgeRun(script, isScript=True):
    """
        Run fledgecontroller with script or string.
        isScript = False : open file is needed to write string(script)
    """

    if not(isScript):
        outfilepath = testoutput + '/fledgerun.fct'
        outfile = open(outfilepath, 'w+')
        outfile.write(script)
        outfile.close()
        os.system('pushd ' + testoutput + ';cmd /C fledgeRun' + \
            device + '.bat ' + outfilepath )
    else:
        log.debug('Running flege controller with ' + script)
        os.system('pushd ' + testoutput + ';cmd /C fledgeRun' + \
            device + '.bat ' + script )

def touch(x, y, execute=True):
    """
        Run fledgecontroller with touch screen at coordinates (x.y)
        isScript = False : open file is needed to write string(script)
    """
    touchString = 'TouchScreenPress(' + str(x) + ',' + str(y) + ',0)' \
        + '\nTouchScreenClick()' \
        + '\nTouchScreenUnclick()' \
        + '\nTouchScreenUnpress(0)\n' 
    if execute:
       fledgeRun(touchString, False)
    else:
        return touchString


def cleanup():
    """ Kill processes started during setup """
    fledgeRun('Exit', False)
    os.system('cmd /C ' + 'taskkill /F /IM fledge.exe')
    os.system('cmd /C ' + 'taskkill /F /IM java.exe')
    os.system('cmd /C ' + 'taskkill /F /IM cmd.exe')
    result = os.popen('ps -aW|grep java').readline()
    if not(result):
        return True
    else:
        raise testlib.OSSystemException('Unable to kill MDS process')
    result = os.popen('ps -aW|grep fledge').readline()
    if not(result):
        return True
    else:
        raise testlib.OSSystemException('Unable to kill simulator process')
