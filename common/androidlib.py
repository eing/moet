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
# Version 1.0

""" 
    An extension to MonkeyRunner tool in Android SDK.
    For MonkeyRunner documentation, pls refer to
    http://developer.android.com/guide/developing/tools/monkeyrunner_concepts.html
"""

__version__ = '1.1'
__license__ = "EPL 1"
__author__ = [ 'Eing Ong @eingong' ]

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import os
import time

device = ''
id = None

# from androidlib import * will import these methods
__all__ = ["backspaces", "home", "menu", "back", "enter", "scroll", \
    "touch", "drag", "record", "playback", "connect", "kill", \
    "screenshot", "launch", "getDevice", "getpid", "connectMonkey", "getId", "setId"]

# Add libraries in to path
try:
    import sys
    sys.path.append('.')
    id = os.getenv('MOET_DEVICEID')
    testroot = os.getenv('MOET')
    testpath = os.path.join(testroot, 'tests')
    sys.path.append(testpath)
    examplespath = os.path.join(testroot, 'examples')
    sys.path.append(examplespath)
    common = os.path.join(testroot, 'common')
    sys.path.append(common)
except:
    print 'Pls add MOET to your environment setting'
    print 'E.g. Mac Terminal : export MOET=/Users/<youruserid>/moet'
    print 'E.g. Windows DOS  : set MOET=C:\moet'


def backspaces(num=1):
    """ Enter backspaces """
    connect()
    while num > 0:
        device.press('KEYCODE_DEL', 'DOWN_AND_UP')
        num = num - 1
    
def home():
    """ Press home key  """
    connect()
    device.press('KEYCODE_HOME', 'DOWN_AND_UP')

def menu():
    """ Press menu key  """
    connect()
    device.press('KEYCODE_MENU', 'DOWN_AND_UP')

def back():
    """ Press back button  """
    connect()
    device.press('KEYCODE_BACK', 'DOWN_AND_UP')

def enter(string=None):
    """ Press enter or enter string  """
    connect()
    if string is None:
        device.press('KEYCODE_ENTER', 'DOWN_AND_UP')
    else:
        strList = string.split()
        strLen = len(strList) - 1
        device.type(strList[0])
        if strLen >= 1:
            index = 1
            while index <= strLen:
                device.press('KEYCODE_SPACE', 'DOWN_AND_UP')
                device.type(strList[index])
                index = index + 1

def scroll(action='left', num=1):
    """ Press cursor keys (up, down, left, right)  """
    connect()
    keymap = { 'up' : 'KEYCODE_DPAD_UP' , 'down' : 'KEYCODE_DPAD_DOWN' , \
        'left' : 'KEYCODE_DPAD_LEFT' , 'right' : 'KEYCODE_DPAD_RIGHT' }
    if action in ['up', 'down', 'left', 'right']:
        key = keymap[action]
        while num > 0:
            device.press(key, 'DOWN_AND_UP')
            num = num - 1

def absCoordinates(percentCoord, type='x'):
    try:
        percentCoord = percentCoord.rstrip('%')
        # attempt to get resolution
        import testlib
        if type == 'x':
            resolution = testlib.settings.resX
        if type == 'y':
            resolution = testlib.settings.resY
    except:
        if type == 'x':
            resolution = 480
        if type == 'y':
            resolution = 800
    return str( int(percentCoord) * int(resolution) / 100)

def touch(posX=0, posY=0, action='default'):
    """ 
        Touch on screen at co-ordinates (posX,posY)
        @param posX integer value or % e.g. 50 or 50%
        @param posY integer value or % e.g. 50 or 50%
    """
    keymap = { 'default' : 'DOWN_AND_UP', 'up' : 'UP', 'down' : 'DOWN' }
    posX = str(posX)
    posY = str(posY)
    # set default resolution
    resX = 480
    resY = 800
    if posX.endswith('%') :
        posX = absCoordinates(posX, 'x')
    if posY.endswith('%'):
        posY = absCoordinates(posY, 'y')
    connect()
    device.touch(int(posX), int(posY), keymap[action])

def drag(fromX=0, fromY=0, toX=0, toY=0):
    """ 
        Move on touch screen from (fromX,fromY) to (toX, toY)
        @param posX integer value or % e.g. 50 or 50%
        @param posY integer value or % e.g. 50 or 50%
    """
    fromX = str(fromX)
    fromY = str(fromY)
    toX = str(toX)
    toY = str(toY)
    if fromX.endswith('%') :
        fromX = absCoordinates(fromX, 'x')
    if fromY.endswith('%'):
        fromY = absCoordinates(fromY, 'y')
    if toX.endswith('%') :
        toX = absCoordinates(toX, 'x')
    if toY.endswith('%'):
        toY = absCoordinates(toY, 'y')
    connect()
    device.drag((int(fromX), int(fromY)), (int(toX), int(toY)), 0.5, 5)

def record(seconds=5, returnResult=False):
    """ 
        Record events 
        @param seconds length of recording time in seconds
    """
    # Start recording i.e. get events
    if id is None:
        adb = 'adb' 
    else:
        adb = 'adb -s ' + id
    eventsfile = 'recordfile'
    eventsFileHandle = open(eventsfile, 'w')
    os.system('> ' + eventsfile)
    cmd = adb + ' shell getevent >& ' + eventsfile + ' &'
    import subprocess
    adbProcess = subprocess.Popen(adb + ' shell getevent', shell=True, stdout=eventsFileHandle)
    #os.system(adb + ' shell getevent >& ' + eventsfile + ' &')
    time.sleep(seconds)
    eventsFileHandle.close()

    # Kill recorder after time elapsed
    if (os.getenv('PATH').find('Program Files')) >= 0:
        # windows
        # This is for cygwin
        #pscmd='ps -s '
        os.system('cmd /C taskkill /F /IM getevent')
    else:
        pids = subprocess.Popen(['ps','-A'], stdout=subprocess.PIPE)
        out = pids.communicate()[0].splitlines()
        for line in out:
            if 'getevent' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, 9)
    print('... recording stopped')

    # Translate events for input
    eventsFileHandle = open(eventsfile, 'r')
    events = eventsFileHandle.readlines()
    eventsFileHandle.close()

    index = 0
    eventslen = len(events)
    returnList = []
    while index < eventslen:
        translatedLine = translate(events[index])
        if translatedLine.startswith('sendevent') :
            returnList.append(translatedLine.strip())
        index = index + 1

    # Write events to file for playback
    eventsfile = 'playbackfile'
    os.system('> ' + eventsfile)
    eventsFileHandle = open(eventsfile, 'w')
    for event in returnList:
        eventsFileHandle.write(event + '\n')
    eventsFileHandle.close()
 
    # clean up
    #os.system('rm ' + pidfile)

    # Return events for playback
    if returnResult:
        return ";".join(returnList)

def striplist(l):
    return([x.strip() for x in l])

def playback(events='playbackfile'):
    """ 
        Playback events
    """
    if len(events) < 30:
        # events is a filename
        eventsFileHandle = open(events, 'r')
        events = eventsFileHandle.readlines()
        events = striplist(events)
        eventsFileHandle.close()
    else:
        events = events.split(';')

    # run subset of commands
    eventslen = len(events)
    index = 0
    count = 0
    menuKey = False
    if id is None:
        adb = 'adb' 
    else:
        adb = 'adb -s ' + id
    cmdshell = adb + ' shell "'
    cmd = cmdshell
    while index < eventslen:
        event = events[index]
        cmd = cmd + event + ';'
        if event.find('330') >= 0: 
            count = count + 1
        elif event.find('229') >= 0:
            # slow keys like menu requires sleep
            if event[len(event) - 1] == '0':
                count = 2
                menuKey = True
        elif event.find('0 0 0') >= 0:
            if count == 0:
                count = 2

        if (len(cmd) > 950) or (count == 2):
            cmd = cmd + '"'
            if menuKey :
                time.sleep(5)
            os.system(cmd)
            cmd = cmdshell
            count = 0
            menuKey = False
        index  = index + 1

    # run the last command
    if len(cmd) > len(cmdshell):
        cmd = cmd + '"'
        os.system(cmd)
        time.sleep(3)

def kill(processName):
    id = getId()
    if id is None:
        ADB = 'adb '
    else:
        ADB = 'adb -s ' + id
    cmd = ' shell kill ' + str(getpid(None, processName))
    os.system(ADB + cmd)
    time.sleep(1)

def connect(serialnum=None):
    """ connects to first device or simulator  """
    device = getDevice()
    if not serialnum is None:
        setId(serialnum)
    if device == '':
        connectMonkey()
    return device

def getpid(idIn=None, processName='com.android.commands.monkey'):
    try:
        import subprocess
        if idIn is None:
            id = getId()
        else:
            id = idIn
        if id is None:
            cmd = 'adb shell ps'
        else:
            cmd = 'adb -s ' + id + ' shell ps'
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = result.communicate()[0].splitlines()
        pid = int(filter(lambda p: len(p) == 9 and p[8] == processName, map(lambda l: l.split(), result))[0][1])
        #print 'in getpid'
        #print pid
        if not pid is None:
            return pid
        if id is None:
            cmd = 'adb start-server'
        else:
            cmd = 'adb -s ' + id + ' start-server'
        subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE)
    except:
        #print 'in getpid except'
        if id is None:
            cmdstart = 'adb shell exit'
        else:
            cmdstart = 'adb -s ' + id + ' shell exit'
        subprocess.Popen(cmdstart , shell=True, stdout=subprocess.PIPE)
        pid = None
    return pid

def connectMonkey():

    id = getId()
    device = getDevice()
    from java.io import File, PrintStream, ByteArrayOutputStream
    from java.lang import System
    outFile = ByteArrayOutputStream(100)
    errFile = ByteArrayOutputStream(100)
    System.setOut(PrintStream(outFile))
    System.setErr(PrintStream(errFile))

    # Helps start adb if not started
    # pid of monkeyrunner only exists starting sdk 2.3
    pid = getpid()
    if id is None:
        device = MonkeyRunner.waitForConnection()
    else:
        device = MonkeyRunner.waitForConnection(20, id)

    if pid is None:
        if outFile.size() > 0:
            # call connect again
            if id is None:
                device = MonkeyRunner.waitForConnection()
            else:
                device = MonkeyRunner.waitForConnection(20, id)
    print device
    # Need 2nd connection calls to get the device 
    # see defect http://code.google.com/p/android/issues/detail?id=16722 
    #if id is None:
    #    device = MonkeyRunner.waitForConnection()
    #else:
    #    device = MonkeyRunner.waitForConnection(20, id)

    setDevice(device)
    return device

def screenshot(imagefile='test'):
    """ Takes screenshot of current connection of device or emulator """
    """
    Comment this out as monkeyrunner has issues for OS 2.2 for screenshots
    connect()
    image = device.takeSnapshot()
    try:
        import testlib
        testoutput = testlib.settings.testoutput
        filepath = os.path.join(testoutput, imagefile + '.png')
        # create testoutput if does not exists
        if not os.path.exists(testoutput):
           os.makedirs(testoutput) 
        image.writeToFile(filepath, 'png')
        print imagefile + '.png is saved to ' + filepath
    except:
        filepath = imagefile + '.png'
        image.writeToFile(filepath, 'png')
        print imagefile + '.png is saved to current directory'
    """
    global common
    serialnum = getId()
    if not serialnum is None:
        serialnum = ' -s ' + serialnum + ' '
    else:
        serialnum = ''
    ddmlib=os.path.join(common, 'ddmlib.jar')
    screenshotjar=os.path.join(common, 'screenshot.jar')
    if (os.getenv('PATH').find('Program Files')) >= 0:
        classpath= ddmlib + ";" + screenshotjar
    else:
        classpath= ddmlib + ":" + screenshotjar
    try:
        import testlib
        testoutput = testlib.settings.testoutput
        # create testoutput if does not exists
        if not os.path.exists(testoutput):
           os.makedirs(testoutput)
        imagefullpath = os.path.join(testoutput, imagefile + '.png')
        cmd= "java -cp '" + classpath + "' com.android.screenshot.Screenshot " + serialnum + imagefullpath
        import subprocess
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print imagefile + '.png is saved to ' + testoutput
    except:
        cmd= "java -cp '" + classpath + "' com.android.screenshot.Screenshot " + serialnum + imagefile + '.png'
        import subprocess
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print imagefile + '.png is saved to current directory'
    # wait for file to be saved
    time.sleep(1)

def launch(appActivity):
    """ Launch your application """
    connect()
    #device.startActivity(appActivity)
    device.shell(' am start -n ' + appActivity)

def translate(inputString):
    """
       Translates an list of adb getevents to adb sendevent for playback
       E.g.
          Input  : /dev/input/event0: 0001 00e5 00000001
          Output : sendevent /dev/input/event0 1 229 1
    """
    colonSplit = inputString.split(':')
    if len(colonSplit) < 2:
        return ''
    spaceSplit = colonSplit[1].split()
    if len(spaceSplit) < 3:
        return ''
    base = 16
    command = 'sendevent ' 

    deviceList = colonSplit[0].split('/')
    device = '/' + deviceList[1] + '/' + deviceList[2]  + '/' + deviceList[3] \
        +  ' '
    type = str(int(spaceSplit[0], base)) + ' '
    code = int(spaceSplit[1], base)
    value = str(int(spaceSplit[2], base))

    code = str(code) + ' '
    outputString = command + device + type + code + value
    return outputString

def getDevice():
    """ Returns MonkeyDevice """
    global device
    return device

def setDevice(deviceIn):
    """ Sets MonkeyDevice """
    global device
    device = deviceIn 

def getId():
    """ Returns Device ID"""
    global id
    return id

def setId(idIn):
    """ Sets MonkeyDevice """
    global id
    id = idIn 
