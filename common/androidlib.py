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
    Library containing all Android device common functions. 
"""

import os
import time
import telnetlib
import translate

serialnum=os.getenv('ANDROID_SERIAL')
ADB='adb '
isSimulator=True

if not serialnum is None:
    ADB='adb -s ' + serialnum + ' '
    if serialnum.find('emulator') < 0:
        isSimulator=False
else:
    serialnum=''
    grep=os.popen('adb get-serialno')
    if grep.readline().find('emulator') < 0:
        isSimulator=False
    grep.close()
session = None
keycode = { \
    "1"         : 2, \
    "2"         : 3, \
    "3"         : 4, \
    "4"         : 5, \
    "5"         : 6, \
    "6"         : 7, \
    "7"         : 8, \
    "8"         : 9, \
    "9"         : 10, \
    "0"         : 11, \
    "q"         : 16, \
    "w"         : 17, \
    "e"         : 18, \
    "r"         : 19, \
    "t"         : 20, \
    "y"         : 21, \
    "u"         : 22, \
    "i"         : 23, \
    "o"         : 24, \
    "p"         : 25, \
    "a"         : 30, \
    "s"         : 31, \
    "d"         : 32, \
    "f"         : 33, \
    "g"         : 34, \
    "h"         : 35, \
    "j"         : 36, \
    "k"         : 37, \
    "l"         : 38, \
    "z"         : 44, \
    "x"         : 45, \
    "c"         : 46, \
    "v"         : 47, \
    "b"         : 48, \
    "n"         : 49, \
    "m"         : 50, \
    "."         : 52, \
    "@"         : 215, \
    "/"         : 53, \
    ","         : 51, \
    "alt"       : 56, \
    "sym"       : 127, \
    "shift"     : 42, \
    "delete"    : 14, \
    "enter"     : 28, \
    "space"     : 57, \
    "home"      : 102, \
    "up"        : 103, \
    "left"      : 105, \
    "right"     : 106, \
    "down"      : 108, \
    "endcall"   : 107, \
    "power"     : 116, \
    "back"      : 158, \
    "menu"      : 229, \
    "call"      : 231
}

altkeys = { \
    '!':1 , '#':3 , '$':4 , '%':5 , '^':6 , '&':7 , \
    '*':8 , '(':9 , ')':0 , '|':'q' , '~':'w' , \
    '"':'e' , '`':'r' , '{':'t' , '}':'y' , '-':'u' , \
    '+':'o' , '=':'p' , '\\':'s' , '\'':'d' , '[':'f' , \
    ']':'g' , '<':'h' , '>':'j' , ';':'k' , ':':'l' , \
    '?':'/' 
}


def startSession(host='localhost', port = '5554'):
    """
        Start telnet session into Android simulator.
        @param host : hostname, default localhost
        @param port : telnet port, default 5554
    """ 
    global session
    if session is None:
        session = telnetlib.Telnet(host, port)

def closeSession():
    """ Close telnet session """
    global session
    if not session is None:
        session.close()
        session = None

def executeKeyEvent(keycode, run=True):
    """ Takes event integer keycode and excecute"""
    event = 'event4'
    if isSimulator:
        event = 'event0'
    cmd = 'sendevent /dev/input/' + event + ' 1 ' + str(keycode) + ' 1;' \
        + 'sendevent /dev/input/' + event + ' 1 ' + str(keycode) + ' 0' 
    if run:
        cmd = ADB + 'shell "' + cmd + '"' 
        os.system(cmd)
    else:
        return cmd + ';'

def backspaces(num=1):
    """ Enter backspaces into simulator """
    startcmd = ADB + 'shell "' 
    event = 'event4'
    if isSimulator:
        event = 'event0'
    cmd = startcmd
    deleteKey = str(keycode['delete'])
    count = 0
    while num > 0:
        cmd = cmd + \
            'sendevent /dev/input/' + event + ' 1 ' + deleteKey +  ' 1;' \
            'sendevent /dev/input/' + event + ' 1 ' + deleteKey + ' 0;' 
        count = count + 1
        if count > 12:
            count = 0
            cmd = cmd + '"'
            os.system(cmd)
            cmd = startcmd
        num = num - 1
    if count > 0:
        cmd = cmd + '"'
        os.system(cmd)
    
def home():
    """ Press home key in simulator """
    if isSimulator:
        executeKeyEvent(keycode['home'])
    else:
        touch(700,1000)

def menu():
    """ Press menu key in simulator """
    if isSimulator:
        executeKeyEvent(keycode['menu'])
    else:
        touch(400,1000)

def back():
    """ Press back button in simulator """
    if isSimulator:
        executeKeyEvent(keycode['back'])
    else:
        touch(100,1000)

def enter(string=None):
    """ Press enter or enter string in simulator """
    if string is None:
        executeKeyEvent(keycode['enter'])
    else:
        startcmd = ADB + ' shell "' 
        cmd = ''
        size = len(string)
        i = 0 
        runCount = 7
        while i < size:
             key = string[i]
             if key == ' ':
                 key = 'space'
             elif key.isupper():
                 # press the shift key
                 cmd = cmd + executeKeyEvent(keycode['shift'], False)
                 key = key.lower()
             elif key in altkeys:
                 cmd = cmd + executeKeyEvent(keycode['alt'], False)
                 key = str(altkeys[key])
             cmd = cmd + executeKeyEvent(keycode[key], False)
             i = i + 1
             runCount = runCount - 1
             if runCount == 0:
                 cmd = startcmd + cmd + '"'
                 os.system(cmd)
                 cmd = ''
                 runCount = 6
        if cmd <> '' :
            cmd = startcmd + cmd + '"'
            os.system(cmd)

        # This used to work in 2.7
        #startSession()
        #cmd = "event text " + string + "\n"
        #session.write(cmd)

def scroll(action='left', num=1):
    """ Press cursor keys (up, down, left, right) in simulator """
    runCount = 6
    startcmd = ADB + 'shell "' 
    cmd = ''
    while num > 0:
        if action in ['up', 'down', 'left', 'right']:
            cmd = cmd + executeKeyEvent(keycode[action], False)
        num = num - 1
        runCount = runCount - 1
        if runCount == 0:
            cmd = startcmd + cmd + '"'
            os.system(cmd)
            cmd = ''
            runCount = 6
    if cmd <> '' :
        cmd = startcmd + cmd + '"'
        os.system(cmd)


def touch(posX=0, posY=0, action='default'):
    """ 
        Touch on screen at co-ordinates (posX,posY)
    """
    posX = str(posX)
    posY = str(posY)
    cmd = ADB + 'shell "'
    if isSimulator:
        touch = \
            'sendevent /dev/input/event0 3 0 ' + posX + ';' \
            + 'sendevent /dev/input/event0 3 1 ' + posY + ';' \
            + 'sendevent /dev/input/event0 1 330 1;'
        release = \
            'sendevent /dev/input/event0 0 0 0;' \
            + 'sendevent /dev/input/event0 1 330 0;' \
            + 'sendevent /dev/input/event0 0 0 0'
    else:
        touch = \
            'sendevent /dev/input/event3 3 48 1;' \
            + 'sendevent /dev/input/event3 3 53 ' + posX + ';' \
            + 'sendevent /dev/input/event3 3 54 ' + posY + ';' \
            + 'sendevent /dev/input/event3 0 2 0;' \
            + 'sendevent /dev/input/event3 0 0 0;'
        release = \
            'sendevent /dev/input/event3 3 48 0;' \
            + 'sendevent /dev/input/event3 0 2 0;' \
            + 'sendevent /dev/input/event3 0 0 0'

    if action == 'down':
        cmd = cmd + touch
    elif action == 'up':
        cmd = cmd + release
    else:
        cmd = cmd + touch + release
    cmd = cmd + '"' 
    os.system(cmd)


def drag(fromX=0, fromY=0, toX=0, toY=0):
    """ 
        Move on touch screen from (fromX,fromY) to (toX, toY)
    """
    if isSimulator:
        release = 'sendevent /dev/input/event0 0 0 0'
    else:
        release = 'sendevent /dev/input/event3 0 2 0;' \
            + 'sendevent /dev/input/event3 0 0 0' 
    os.system(ADB + 'shell "' + release + '"')

    if isSimulator:
        cmd = ADB + 'shell "' \
            + 'sendevent /dev/input/event0 3 0 ' + str(fromX) + ';' \
            + 'sendevent /dev/input/event0 3 1 ' + str(fromY) + ';' \
            + 'sendevent /dev/input/event0 1 330 1;' \
            + 'sendevent /dev/input/event0 0 0 0;'
    else:
        cmd = ADB + 'shell "' \
            + 'sendevent /dev/input/event3 3 48 1;' \
            + 'sendevent /dev/input/event3 3 50 2;' \
            + 'sendevent /dev/input/event3 3 53 ' + str(fromX) + ';' \
            + 'sendevent /dev/input/event3 3 54 ' + str(fromY) + ';' \
            + 'sendevent /dev/input/event3 0 2 0;' \
            + 'sendevent /dev/input/event3 0 0 0;'
    diffX = toX - fromX
    diffY = toY - fromY
     
    stepX = -200
    stepY = -200
    if diffX > 0:
        stepX = abs(stepX) 
    if diffY > 0:
        stepY = abs(stepY)
    totalX = diffX / stepX
    totalY = diffY / stepY

    while ((totalX > 0) or (totalY > 0)):
        if totalX > 0:
            totalX = totalX - 1
            fromX = fromX + stepX
            if isSimulator:
                cmd = cmd + 'sendevent /dev/input/event0 3 0 ' + str(fromX) + ';'
            else:
                cmd = cmd \
                    + 'sendevent /dev/input/event3 3 48 1;' \
                    + 'sendevent /dev/input/event3 3 50 2;' \
                    + 'sendevent /dev/input/event3 3 53 ' + str(fromX) + ';'

        if totalY > 0:
            totalY = totalY - 1
            fromY = fromY + stepY
            if isSimulator:
                cmd = cmd + 'sendevent /dev/input/event0 3 1 ' + str(fromY) + ';'
            else:
                cmd = cmd + 'sendevent /dev/input/event3 3 54 ' + str(fromY) + ';'
        if isSimulator:
            cmd = cmd + 'sendevent /dev/input/event0 0 0 0;'
        else:
            cmd = cmd + 'sendevent /dev/input/event3 0 2 0;sendevent /dev/input/event3 0 0 0;'

    if isSimulator:
        cmd = cmd \
            + 'sendevent /dev/input/event0 3 0 ' + str(toX) + ';' \
            + 'sendevent /dev/input/event0 3 1 ' + str(toY) + ';' \
            + 'sendevent /dev/input/event0 0 0 0;' \
            + 'sendevent /dev/input/event0 1 330 0;'
    else:
        cmd = cmd \
            + 'sendevent /dev/input/event3 3 48 1;' \
            + 'sendevent /dev/input/event3 3 50 2;' \
            + 'sendevent /dev/input/event3 3 53 ' + str(toX) + ';' \
            + 'sendevent /dev/input/event3 3 54 ' + str(toY) + ';' \
            + 'sendevent /dev/input/event3 0 2 0;' \
            + 'sendevent /dev/input/event3 0 0 0;' + release
    os.system(cmd + '"')

def record(seconds=5, returnResult=False):
    """ 
        Record events on simulator 
        @param seconds length of recording time in seconds
    """
    # Start recording i.e. get events
    eventsfile = 'recordfile'
    os.system('> ' + eventsfile)
    os.system(ADB + 'shell getevent >& ' + eventsfile + ' &')
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
        translatedLine = translate.translate(events[index])
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
        Playback events on simulator 
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
    cmdshell = ADB + 'shell "'
    cmd = cmdshell
    count = 0
    menuKey = False
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


def setDevice(serial='emulator-5554'):
    """Switch between different devices"""
    global ADB
    global serialnum
    serialnum = serial 
    ADB='adb -s ' + serialnum + ' '
    global isSimulator
    if serialnum.find('emulator') < 0:
        isSimulator=False
    else:
        isSimulator=True

def screenshot(imagefile='test'):
    """Takes screenshot of current connect device or emulator"""
    global serialnum
    serial = ''
    if len(serialnum) <> 0:
        serial = '-s ' + serialnum + ' '
    classpath = os.getenv('CLASSPATH')
    if classpath is None:
        classpath='../common/ddmlib.jar:../common/screenshot.jar:ddmlib.jar:screenshot.jar'
    cmd="java -cp '" + classpath + "' com.android.screenshot.Screenshot " + serial + imagefile + '.png'
    os.system(cmd)

def launch(appActivity):
    """Launch your application"""
    if appActivity is None:
        print "Usage: Provide activityname e.g. com.package.name/com.package.name.ActivityName"
    else:
        cmd = ADB + 'shell am start -n ' + appActivity
        os.system(cmd)
