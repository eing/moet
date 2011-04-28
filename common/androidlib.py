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

__version__ = '1.0'
__license__ = "EPL 1"
__author__ = [ 'Eing Ong @eingong' ]

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import os
import time

device = ''
id = None

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

# from androidlib import * will import these methods
__all__ = ["backspaces", "home", "menu", "back", "enter", "scroll", \
    "touch", "drag", "record", "playback", "connect", "connectFirstDevice", \
    "screenshot", "launch", "getDevice"]

def backspaces(num=1):
    """ Enter backspaces """
    global device
    if device == '' :
        connectFirstDevice()
    while num > 0:
        device.press('KEYCODE_DEL', 'DOWN_AND_UP')
        num = num - 1
    
def home():
    """ Press home key  """
    global device
    if device == '' :
        connectFirstDevice()
    device.press('KEYCODE_HOME', 'DOWN_AND_UP')

def menu():
    """ Press menu key  """
    global device
    if device == '' :
        connectFirstDevice()
    device.press('KEYCODE_MENU', 'DOWN_AND_UP')

def back():
    """ Press back button  """
    global device
    if device == '' :
        connectFirstDevice()
    device.press('KEYCODE_BACK', 'DOWN_AND_UP')

def enter(string=None):
    """ Press enter or enter string  """
    global device
    if device == '' :
        connectFirstDevice()
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
    global device
    if device == '' :
        connectFirstDevice()
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
    global device
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
    if device == '' :
        connectFirstDevice()
    device.touch(int(posX), int(posY), keymap[action])

def drag(fromX=0, fromY=0, toX=0, toY=0):
    """ 
        Move on touch screen from (fromX,fromY) to (toX, toY)
        @param posX integer value or % e.g. 50 or 50%
        @param posY integer value or % e.g. 50 or 50%
    """
    global device
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
    if device == '' :
        connectFirstDevice()
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
    os.system('> ' + eventsfile)
    os.system(adb + ' shell getevent >& ' + eventsfile + ' &')
    time.sleep(seconds)

    # Kill recorder after time elapsed
    pidfile = 'pidfile'

    # This is for cygwin
    pscmd='ps -s '
    if os.system(pscmd + ' >& /dev/null') > 0:
        # For mac or unix
        pscmd='ps '
    os.system(pscmd + '| grep "shell getevent" >& ' + pidfile)
    pidFileHandle = open(pidfile, 'r')
    pid = pidFileHandle.read(20).split()[0]
    pidFileHandle.close()
    print('... recording stopped')
    os.system('kill -9 ' + pid)

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
    os.system('rm ' + pidfile)

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
        
def connect(serialnum):
    """ connect to new serialnum """
    global device
    global id
    if device != '' :
        device = ''
    id = serialnum
    device = MonkeyRunner.waitForConnection(20, id)
    return device

def connectFirstDevice():
    """ connects to first device or simulator  """
    global device
    global id
    if id is None:
        device = MonkeyRunner.waitForConnection(20)
    else:
        device = MonkeyRunner.waitForConnection(20, id)
    return device

def screenshot(imagefile='test'):
    """ Takes screenshot of current connection of device or emulator """
    global device
    if device == '' :
        connectFirstDevice()
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

def launch(appActivity):
    """ Launch your application """
    global device
    if device == '' :
        connectFirstDevice()
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
    return device
