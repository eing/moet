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

""" Compare tool takes a snapshot of the current image and compare 
    with the expected image. 
    (Optional) Cropped settings determines area to compare 
               There are a few crop options -
               1. (Preferred - resolution independent) 100%x80%+10%+20% 
               2. 320x90+0+0 
               3. +0+90
    (Optional) Tolerance is the level of error for failing compare
"""

import os
import shutil


try:
    import logger
    import testlib
    log = logger.getLogger('imagelib')
    testEnv = testlib.testenv
    test_output = testEnv.testoutput
    image_tool = testEnv.imageTool + '/'
    runOption = testEnv.getRunOption()
    resX = testEnv.resX
    resY = testEnv.resY
    imageOutputDir = testEnv.resources
except:
    # Create image.log with DEBUG log level
    logfile="imagelib.log"
    if not os.path.exists(logfile):
        logfileIO = open(logfile, 'a')
        logfileIO.close()
    import logging
    log = logging.getLogger(logfile)
    fileHandler = logging.FileHandler(logfile)
    formatter = logging.Formatter(\
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fileHandler.setFormatter(formatter)
    log.addHandler(fileHandler)
    log.setLevel(logging.DEBUG)
    # Set testEnv variables
    test_output = '.'
    runOption = 'CAPTURE'
    resX = '320'
    resY = '480'
    imageOutputDir = '.'
    # Note. This expects convert and compare tools from ImageMagick be in the SYSTEM PATH
    image_tool = ''
    

def parseCropSettings(cropSettings, resX, resY):
    """ Convert settings in % to actual resolution crop settings, e.g.
        parseCropSettings('320x90+0+0', '320', '240')
        parseCropSettings('100%x90%+10%+0', '320', '240')
        parseCropSettings('320x90%+10+0', '320', '240')
        parseCropSettings('+10+0', '320', '240')
        parseCropSettings('320x90', '320', '240')
        parseCropSettings('+10%+0', '320', '240')
    """

    log.debug('Original crop settings ' + cropSettings)
    percentSignSplit = cropSettings.split('%')
    if len(percentSignSplit) < 2:

        # Case of +0+0, 320x120, 320x120+0+90
        log.debug('No change in cropSettings - ' + cropSettings)
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

    log.debug('Cropping image to ' + newCropSettings)
    return newCropSettings


def compare(device, image, cropSettings=None, tolerance=500):
    """ Compare images using cropped settings and tolerance level """

    if 'getScreenShot' in dir(device) :
        device.getScreenShot(image)
    else:
        # Workaround for devices that have not implemented image capture
        return True

    # crop images before compare if necessary
    actualImage = test_output + '/' + image + '.png'
    expectedImage = imageOutputDir + '/' + resX + 'x' + resY + '/' \
        + image + '.png'

    # if run option is 'CAPTURE', copy images from output to resources dir
    if runOption != "TEST":
        shutil.copy(actualImage, expectedImage)
        return True
    
    if not os.path.exists(actualImage):
        log.debug("Actual image file to compare does not exist")
        return False

    if cropSettings:
        cropSettings = parseCropSettings(cropSettings, resX, resY)
        croppedActualImage = test_output + '/' +  image + 'ActualCropped.png'
        croppedExpectedImage = test_output + '/' + image \
            + 'ExpectedCropped.png'
        convertActual = image_tool + 'convert -crop ' + cropSettings \
            + ' ' + actualImage + ' ' + croppedActualImage
        convertExpected = image_tool + 'convert -crop ' \
            + cropSettings + ' ' + expectedImage + ' ' \
            + croppedExpectedImage

        os.system('cmd /C ' + convertActual)
        os.system('cmd /C ' + convertExpected)
        actualImage = croppedActualImage
        expectedImage = croppedExpectedImage

    # set compare command
    diffImage = test_output + '/' + image + 'Diff.png'
    diffResult = test_output + '/diff.txt'
    compareCall = image_tool + 'compare -verbose -metric AE ' \
        + actualImage + ' ' + expectedImage + ' ' + diffImage \
        + ' 2>' + diffResult

    # diff images
    log.info('Comparing images - ' + compareCall)
    os.system('cmd /C ' + compareCall)
    result = os.popen('grep red ' + diffResult \
        + " | cut -d : -f 2 | cut -d ' ' -f 2").readline()

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
        log.debug("Compare results is invalid")
        return False


if __name__ == "__main__":
    import bb
    b = bb.BlackBerry()
    x = compare(b, 'testCreateCustomerWithNoAddresses', '100%x90%', None)
    print  x

