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

__version__ = '1.0'
__license__ = "EPL 1"
__author__ = [ 'Eing Ong @eingong' ]

import os
path = os.getenv('PATH')
imageCmd = ''
""" Support for windows os """
if path.find('Program Files') >= 0:
    imageCmd = 'cmd \C '

""" Compare tool takes a snapshot of the current image and compare 
    with the expected image. 
    (Optional) Cropped settings determines area to compare 
               There are a few crop options -
               1. (Preferred - resolution independent) 100%x80%+10%+20% 
               2. 320x90+0+0 
               3. +0+90
    (Optional) Tolerance is the level of error for failing compare
"""


# Set variables
test_output = '.'
runOption = 'TEST'
resX = ''
resY = ''
subDir = ''
resourcesDir = '.'
# Note. This expects convert and compare tools from ImageMagick be in the SYSTEM PATH
image_tool = ''

try:
    import testlib
    testEnv = testlib.settings
    test_output = testEnv.testoutput
    resourcesDir = testEnv.resources
    resX = testEnv.resX
    resY = testEnv.resY
    runOption = testEnv.getRunOption()
    image_tool = testEnv.imageTool + '/'
except:
    print

def parseCropSettings(cropSettings, resX, resY):
    """ Convert settings in % to actual resolution crop settings, e.g.
        parseCropSettings('320x90+0+0', '320', '240')
        parseCropSettings('100%x90%+10%+0', '320', '240')
        parseCropSettings('320x90%+10+0', '320', '240')
        parseCropSettings('+10+0', '320', '240')
        parseCropSettings('320x90', '320', '240')
        parseCropSettings('+10%+0', '320', '240')
    """

    percentSignSplit = cropSettings.split('%')
    if len(percentSignSplit) < 2:

        # Case of +0+0, 320x120, 320x120+0+90
        return cropSettings

    else:
        plusSignSplit = cropSettings.split('+')

        if len(plusSignSplit) < 2:
            # Case of 320x10%
            sizeX = (plusSignSplit[0]).split('x')[0].split('%')
            if len(sizeX) > 1:
                sizeX = str( int(sizeX[0]) * int(resX) / 100 )
            else:
                sizeX = sizeX[0]
            sizeY = (plusSignSplit[0]).split('x')[1].split('%')
            if len(sizeY) > 1:
                sizeY = str( int(sizeY[0]) * int(resY) / 100 )
            else:
                sizeY = sizeY[0]
            newCropSettings = sizeX + 'x' + sizeY + '+0+0'

        elif plusSignSplit[0] == '':
            # Case of +0+10%
            positionX = (plusSignSplit[1]).split('%')
            if len(positionX) > 1:
                positionX = str( int(positionX[0]) * int(resX) / 100 )
            else:
                positionX = positionX[0]

            positionY = (plusSignSplit[2]).split('%')
            if len(positionY) > 1:
                positionY = str( int(positionY[0]) * int(resY) / 100 )
            else:
                positionY = positionY[0]
            newCropSettings = '+' + positionX + '+' + positionY

        else:
            # Case of 320x120+0x10%, 90%x10%+0+20%
            sizeX = (plusSignSplit[0]).split('x')[0].split('%')
            if len(sizeX) > 1:
                sizeX = str( int(sizeX[0]) * int(resX) / 100 )
            else:
                sizeX = sizeX[0]

            sizeY = (plusSignSplit[0]).split('x')[1].split('%')
            if len(sizeY) > 1:
                sizeY = str( int(sizeY[0]) * int(resY) / 100 )
            else:
                sizeY = sizeY[0]

            positionX = (plusSignSplit[1]).split('%')
            if len(positionX) > 1:
                positionX = str( int(positionX[0]) * int(resX) / 100 )
            else:
                positionX = positionX[0]

            positionY = (plusSignSplit[2]).split('%')
            if len(positionY) > 1:
                positionY = str( int(positionY[0]) * int(resY) / 100 )
            else:
                positionY = positionY[0]
            newCropSettings = sizeX + 'x' + sizeY + '+' + positionX + '+' + positionY

    return newCropSettings


def compare(image, device=None, cropSettings=None, tolerance=500):
    """ Compare images using cropped settings and tolerance level """

    if not device is None:
        if 'getScreenShot' in dir(device) :
            device.getScreenShot(image)
        elif 'screenshot' in dir(device) :
            device.screenshot(image)
        else:
            # Workaround for devices that have not implemented image capture
            print 'Pls implement getScreenShot(imagename) for your device'
            return True

    # crop images before compare if necessary
    actualImage = os.path.join(test_output, image + '.png')
    expectedImage = os.path.join(resourcesDir, image + '.png')
    #print 'actualImage is ' + actualImage
    #print 'expectImage is ' + expectedImage

    # if run option is 'CAPTURE', copy images from output to resources dir
    if runOption.find('CAPTURE') >= 0 and not device is None:
        expectedImageDir = resourcesDir
        if not os.path.exists(expectedImageDir): 
            os.makedirs(expectedImageDir)
        import shutil
        shutil.copy(actualImage, expectedImage)
        return True
    
    if not os.path.exists(actualImage):
        return False

    if cropSettings:
        cropSettings = parseCropSettings(cropSettings, resX, resY)
        croppedActualImage = os.path.join(test_output, image + 'ActualCropped.png')
        croppedExpectedImage = os.path.join(test_output, image + 'ExpectedCropped.png')
        convertActual = image_tool + 'convert -crop ' + cropSettings \
            + ' ' + actualImage + ' ' + croppedActualImage
        convertExpected = image_tool + 'convert -crop ' \
            + cropSettings + ' ' + expectedImage + ' ' \
            + croppedExpectedImage

        os.system(imageCmd + convertActual)
        os.system(imageCmd + convertExpected)
        actualImage = croppedActualImage
        expectedImage = croppedExpectedImage

    # set compare command
    diffImage = os.path.join(test_output, image + 'Diff.png')
    diffResult = os.path.join(test_output, 'diff.txt')
    compareCall = image_tool + 'compare -verbose -fuzz 5% -metric AE ' \
        + actualImage + ' ' + expectedImage + ' ' + diffImage \
        + ' 2>' + diffResult

    # diff images
    os.system(imageCmd + compareCall)
    grep = os.popen('grep red ' + diffResult \
        + " | cut -d : -f 2 | cut -d ' ' -f 2")
    result = grep.readline()
    grep.close()

    # return pass(True) or fail (False)
    if tolerance is None:
        tolerance = 500 
    try:
        result = int(result)
        if result < tolerance:
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    import bb
    b = bb.BlackBerry()
    print 'resourcesDir is ' + resourcesDir
    x = compare(b, 'testCreateCustomerWithNoAddresses', '100%x90%', None)
    print  x

