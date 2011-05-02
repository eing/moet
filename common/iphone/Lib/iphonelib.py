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
   An extension to Sikuli tool. 
   For Sikuli IDE and documentation, pls refer to 
   http://sikuli.org
"""

__version__ = '1.0'
__license__ = "EPL 1"
__author__ = [ 'Eing Ong @eingong' ]

from sikuli.Sikuli import *
Settings.ActionLogs=False
Settings.InfoLogs=False
Settings.DebugLogs=False


# Add image paths and optimize image matching to just iphone simulator
try:
    import os, sys
    demo = os.getenv('MOET_MODE')
    if demo.find('DEMO') >= 0:
        demo = True
    else:
        demo = False
    pathCheck = False 
    testroot = os.getenv('MOET')
    commonImages = os.path.join(testroot, 'common', 'iphone')
    testsImages = os.path.join(testroot, 'resources', 'iphone', '320x480')
    addImagePath(commonImages) 
    addImagePath(testsImages)
    testpath = os.path.join(testroot, 'tests')
    sys.path.append(testpath)
    examplespath = os.path.join(testroot, 'examples')
    sys.path.append(examplespath)
    common = os.path.join(testroot, 'common')
    sys.path.append(common)
    pathCheck = True 

    originalLoc = Env.getMouseLocation()
    region = find('iPhoneHeader.png')
    myRect = region.getRect()
    (regX, regY, w, h) = (myRect.x - 10, myRect.y, myRect.width + 10, myRect.height + 20)
    region = Region(regX, regY, w, 700)
    setRect(region)
    screenOffsetX = 10
    screenOffsetY = 115

except:
    if not pathCheck:
        print 'Pls add TEST_ROOT to your environment setting'
        print 'E.g. Mac Terminal : export TEST_ROOT=/Users/<youruserid>/moet'
        print 'E.g. Windows DOS  : set TEST_ROOT=C:\moet'
    else:
        print 'Pls make sure your device simulator is in the foreground'


def resetCurrentLocation():
    global originalLoc
    if demo:
        click(originalLoc)

def home():
    """ Enter Home button """
    if demo:
         click("iPhoneHeader.png")
    keyDown(Key.SHIFT)
    keyDown(Key.META)
    keyDown('h')
    keyUp(Key.META)
    keyUp(Key.SHIFT)
    keyUp('h')
    resetCurrentLocation()

def backspaces(num = 1):
    """ Enter backspaces """
    if demo:
         click("iPhoneHeader.png")
    while num > 0:
        num = num - 1
        keyDown(Key.BACKSPACE)
        keyUp(Key.BACKSPACE)
    resetCurrentLocation()

def enter(string):
    if demo:
         click("iPhoneHeader.png")
    type(string)
    resetCurrentLocation()

def zoom(action='out',fromX=50, fromY=300, step=1):
    if demo:
         click("iPhoneHeader.png")
    x = fromX - (10 * step)
    if x < 0:
        x = 10
    y = fromY + (10 * step) 
    if y > 480:
        y = 450
    if action == 'out':
        toX = fromX
        toY = fromY
        fromX = x
        fromY = y
    else:
        toX = x
        toY = y
    region.keyDown(Key.ALT)
    region.drag(Location(regX + screenOffsetX + fromX, regY + screenOffsetY + fromY))
    region.dropAt(Location(regX + screenOffsetX + toX, regY + screenOffsetY + toY))
    region.keyUp(Key.ALT)
    resetCurrentLocation()


def absCoordinates(percentCoord, type='x'):
    percentCoord = percentCoord.rstrip('%')
    if type == 'x':
        resolution = 320
    if type == 'y':
        resolution = 480
    return  (int(percentCoord) * int(resolution) / 100)
        
def touch(x, y):    
    """
        Touch on screen at co-ordinates (posX,posY)
        @param posX integer value or % e.g. 50 or 50%
        @param posY integer value or % e.g. 50 or 50%
    """
    posX = str(x)
    posY = str(y)
    # set default resolution
    if posX.endswith('%') :
        posX = absCoordinates(posX, 'x')
    if posY.endswith('%'):
        posY = absCoordinates(posY, 'y')
    region.click(Location(regX + screenOffsetX + int(posX), regY + screenOffsetY + int(posY)))
    resetCurrentLocation()

def touchImage(image):
    """
        Touch on screen at image
        @param image image file name
    """
    region.click(image + '.png')
    resetCurrentLocation()

def drag(fromX, fromY, toX, toY):
    """
        Drag on screen from (fromX,fromY) to (toX, toY)
        @param fromX integer value or % e.g. 50 or 50%
        @param fromY integer value or % e.g. 50 or 50%
        @param toX integer value or % e.g. 50 or 50%
        @param toY integer value or % e.g. 50 or 50%
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
    region.drag(Location(regX + screenOffsetX + int(fromX), regY + screenOffsetY + int(fromY)))
    region.dropAt(Location(regX + screenOffsetX + int(toX), regY + screenOffsetY + int(toY)))
    resetCurrentLocation()

def previous():
    """ Click on Previous in keyboard """
    region.click()
    resetCurrentLocation()
            
def next():
    """ Click on Next in keyboard """
    region.click("KeyNext.png")
    resetCurrentLocation()
                
def done():
    """ Click on Done in keyboard """
    region.click("KeyDone.png")
    resetCurrentLocation()

def search():
    """ Click on Search in keyboard """
    region.click("KeySearch.png")
    resetCurrentLocation()

def cancel():
    """ Click on Cancel in keyboard """
    region.click("KeyCancel.png")
    resetCurrentLocation()

def scroll(action, numScrolls=1):
    """ Scroll up, down, left, right numScroll times"""
    if not action in ['up', 'down', 'left', 'right']:
        print 'Only up/down/left/right is supported' 
        return
    # default : down
    xStart = 20
    xEnd = 20
    yStart = 250
    yEnd = 100
    if action == 'up' : 
        yStart = 100
        yEnd = 250
    if action == 'left' : 
        xStart = 120
        yEnd = yStart
    if action == 'right' : 
        xEnd = 120
        yEnd = yStart
    while numScrolls > 0:
        numScrolls = numScrolls - 1
        region.drag(Location(regX + screenOffsetX + xStart, regY + screenOffsetY + yStart))
        region.dropAt(Location(regX + screenOffsetX + xEnd, regY + screenOffsetY + yEnd))
    resetCurrentLocation()
    
def screenshot(filename='test'):
    """ Saves screenshot to your current working directory or TEST_OUTPUT if exists """
    import os, shutil
    myRect = region.getRect()
    imageRegion = Region(myRect.x + 17, myRect.y + 134,\
        myRect.width - 37, myRect.height - 238)
    image = capture(imageRegion)
    # appends .png to input filename if needed
    if filename.find('png') < 0 : 
        filename = filename + '.png'
    try:
        import testlib
        testoutput = testlib.settings.testoutput
        filepath = os.path.join(testoutput, filename)
        # create testoutput if not exists
        if not os.path.exists(testoutput):
            os.makedirs(testoutput)
        # move image there
        shutil.move(image, os.path.join(testoutput, filename))
        print filename + ' is saved to ' + filepath
    except:
        shutil.move(image, os.path.join(os.getcwd(), filename))
        print filename + ' is saved to current directory'

def pickerScroll(fieldX, scroll):
    import time
    if scroll < 0:
           scroll = abs(scroll)
           while scroll > 10:
               scroll = scroll - 10
               drag(fieldX, '60%', fieldX, '105%')
               time.sleep(1)
           dragSize = [ ('80%','80%'), ('55%','65%'), ('55%', '75%'), ('55%','85%'), \
               ('55%','95%'), ('55%','100%'), ('60%', '102%'), ('60%', '103%'), \
               ('65%','107%'), ('58%','104%'), ('60%', '105%')]
           drag(fieldX, dragSize[scroll][0], fieldX, dragSize[scroll][1])
    elif scroll > 0:
           while scroll > 10:
               scroll = scroll - 10
               drag(fieldX, '90%', fieldX, '1%')
               time.sleep(1)
           dragSize = [ ('80%','80%'), ('90%','80%'), ('90%', '70%'), ('90%','60%'), \
                   ('90%','50%'), ('90%','42%'), ('90%', '35%'), ('90%', '28%'), \
                   ('90%', '20%'), ('90%', '10%'), ('90%', '1%')]
           drag(fieldX, dragSize[scroll][0], fieldX, dragSize[scroll][1])


def picker(field1, field2=0, field3=0):
    """ 
        Use for selecting UI scroll pickers (e.g. datePicker)
        @param field1 Leftmost field. 1 to move down one notch, -1 to move up a notch.
        @param field2 Second field, default is 0
        @param field3 Last field, default is 0
    """
    global demo
    tmp = demo
    demo = False
    if (field1 != 0):
       fieldX = '20%'
       pickerScroll(fieldX, field1)
    if field2 != 0:
       fieldX = '70%'
       pickerScroll(fieldX, field2)
    if field3 != 0:
       fieldX = '90%'
       pickerScroll(fieldX, field3)
    demo = tmp
    resetCurrentLocation()
   

def setDemo(value=False):
    global demo
    demo = value
