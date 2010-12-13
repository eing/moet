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

import os
import applib
import appbase
from bblib import *

class StormImpl(appbase.AppInterface):
    """
        Storm implementation of the business rule methods
        specified in interface class CMInterface.
    """
    log = logger.getLogger('StormImpl', __module__)

    def launch(self):
        """ Launch contact manager app"""
        deviceStr = \
            escape(False) \
            + touch(200, 300, False)
        self.log.info('Launch command:\n' + deviceStr)
        fledgeRun(deviceStr, False)


    def add(self, contact=None, options='save'):
        """ Add contact """

        if contact is None:
            contact = applib.Contact()
            contact.setFirstname('BlackBerry')
            contact.setLastname('DevCon')

        deviceStr = \
            touch(100, 50, False) \
            + enter(contact.getFirstname(), False) \
            + pause(1, False) \
            + thumbwheel('down', 1, False) \
            + pause(1, False) \
            + enter(contact.getLastname(), False) \
            + pause(1, False)

        if contact.getPhone() == '':
            # no phone  
            if contact.getEmail() <> '':
                # add email  
                deviceStr = deviceStr \
                    + thumbwheel('down', 7, False) \
                    + enter(contact.getEmail(), False) \
                    + pause(1, False)
        else :
            # add phone
            if contact.getEmail() <> '':
                # add email  
                deviceStr = deviceStr \
                    + thumbwheel('down', 7, False) \
                    + enter(contact.getEmail(), False) \
                    + pause(1, False) \
                    + thumbwheel('down', 6, False) \
                    + enter(contact.getPhone(), False)
            else:
                deviceStr = deviceStr \
                    + thumbwheel('down', 13, False) \
                    + enter(contact.getPhone(), False)

        deviceStr = deviceStr + menu(False)

        if options == 'save':
            deviceStr = deviceStr \
                + touch(50, 300, False) \
                + pause(1, False) \
                + touch(180, 220, False) \
                + pause(1, False) 
        else:
            deviceStr = deviceStr \
                + thumbwheel('down', 6, False) \
                + touch(50, 450, False) \
                + pause(1, False) \
                + touch(180, 280, False) \
                + pause(1, False) 
        self.log.info('Add command:\n' + deviceStr)
        fledgeRun(deviceStr, False)


    def find(self, contact=None, options='save'):
        """ Find contact """

        searchString = contact
        if not isinstance(contact, str):
            searchString = contact.getFirstname() 
        deviceStr = \
            touch(100, 20, False) \
            + pause(1, False) \
            + enter(searchString, False) \
            + touch(200, 100, False) \
            + pause(1, False)

        if options.startswith('del'):
            deviceStr = deviceStr \
                + touch(250, 450, False) \
                + pause(1, False) \
                + touch(150, 250, False) \
                + pause(1, False) \
                + escape(False) \
                + pause(1, False) 
        fledgeRun(deviceStr, False)

        
    def delete(self, execute=True):
        """ Delete loaded contact """

        deviceStr = touch(250, 450, False) \
            + pause(1, False) \
            + touch(150, 250, False) \
            + pause(1, False) \
            + escape(False) \
            + pause(1, False)
        """
        deviceStr = \
            touch(180, 450, False) \
            + pause(1, False) \
            + touch(150, 250, False) \
            + pause(1, False)
        """
        if execute:
            fledgeRun(deviceStr, False)
        else:
            return deviceStr 


    def getScreenShot(self, image):
        """ 
            Get screenshot and save as image name. 
            This is required for common\imagelib.py to work.
            @param image : Name of image to save screenshot
        """
        os.system('cmd /C ' + testlib.testenv.testoutput \
            + '/getScreenShot' + self.device + '.bat ' + image)
