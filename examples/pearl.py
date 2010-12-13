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

class PearlImpl(appbase.AppInterface):
    """
        Pearl implementation of the business rule methods
        specified in interface class CMInterface.
    """
    log = logger.getLogger('PearlImpl', __module__)

    def launch(self):
        """ Launch contact manager app"""
        deviceStr = \
            escape(False) \
            + menu(False) \
            + thumbwheel('down',5, False) \
            + enter(None, False)
        self.log.info('Launch command:\n' + deviceStr)
        fledgeRun(deviceStr, False)


    def add(self, contact=None, options='save'):
        """ Add contact """

        if contact is None:
            contact = applib.Contact()
            contact.setFirstname('BlackBerry')
            contact.setLastname('DevCon')

        deviceStr = \
            menu(False) \
            + enter(None, False) \
            + pause(1, False) \
            + enter(contact.getFirstname(), False) \
            + pause(1, False) \
            + thumbwheel('down', 1, False) \
            + pause(1, False) \
            + enter(contact.getLastname(), False) 

        if contact.getPhone() == '':
            # no phone  
            if contact.getEmail() <> '':
                # add email  
                deviceStr = deviceStr \
                    + thumbwheel('down', 4, False) \
                    + enter(contact.getEmail(), False) \
                    + pause(1, False) \
                    + enter(None, False) \
                    + pause(1, False)
        else :
            # add phone
            if contact.getEmail() <> '':
                # add email  
                deviceStr = deviceStr \
                    + thumbwheel('down', 4, False) \
                    + enter(contact.getEmail(), False) \
                    + pause(1, False) \
                    + enter(None, False) \
                    + pause(1, False) \
                    + thumbwheel('down', 5, False) \
                    + enter(contact.getPhone(), False)
            else:
                deviceStr = deviceStr \
                    + thumbwheel('down', 9, False) \
                    + enter(contact.getPhone(), False)

        if options == 'save':
            deviceStr = deviceStr \
                + menu(False) \
                + pause(1, False) \
                + enter(None, False)
        else:
            deviceStr = deviceStr \
                + escape(False) \
                + thumbwheel('down', 1, False) \
                + enter(None, False)
        self.log.info('Add command:\n' + deviceStr)
        fledgeRun(deviceStr, False)


    def find(self, contact=None, options='None'):
        """ Find contact """

        searchString = contact
        if not isinstance(contact, str):
            searchString = contact.getFirstname() 
        deviceStr = \
            enter(searchString, False) \
            + enter(None, False) 

        if options.startswith('del'):
            deviceStr = deviceStr \
                + menu(False) \
                + thumbwheel('down', 1, False) \
                + enter(None, False) \
                + pause(1, False) \
                + thumbwheel('up', 1, False) \
                + enter(None, False) \
                + pause(1, False) \
                + escape(False) \
                + pause(1, False)
        fledgeRun(deviceStr, False)
        
    def delete(self, execute=True):
        """ Delete loaded contact """

        deviceStr = \
            menu(False) \
            + thumbwheel('down', 1, False) \
            + enter(None, False) \
            + pause(1, False) \
            + thumbwheel('up', 1, False) \
            + enter(None, False) \
            + pause(1, False) \
            + escape(False) \
            + pause(1, False)
        if execute:
            fledgeRun(deviceStr, False)
        else:
            return deviceStr 

    def deleteAutotext(self, size=1):
        """ Delete auto text words """
        deviceStr = \
            menu(False) \
            + thumbwheel('down', 1, False) \
            + enter(None, False) \
            + enter(None, False) \
         
        i = 0
        while (i < size) : 
            deviceStr = deviceStr + deviceStr + deviceStr + deviceStr \
                + deviceStr + deviceStr + deviceStr + deviceStr
            fledgeRun(deviceStr, False)
            i = i + 1


    def getScreenShot(self, image):
        """ 
            Get screenshot and save as image name. 
            This is required for common\imagelib.py to work.
            @param image : Name of image to save screenshot
        """
        os.system('cmd /C ' + testlib.testenv.testoutput \
            + '/getScreenShot' + self.device + '.bat ' + image)
