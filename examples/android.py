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
import time
import applib
import appbase
from androidlib import *

class AndroidImpl(appbase.AppInterface):
    """
        Android implementation of methods specified in interface class.
    """

    def getScreenShot(self, file='test'):
        """ Takes screenshot of current device
            @param file filename with no extension as file will be named file.png
        """
        screenshot(file)

    def launch(self):
        """ Launch app """
        launch('com.android.contacts/.DialtactsContactsEntryActivity -a android.intent.action.MAIN')

    def screen(self, name="phone"):
        """ Navigate to different screens
            @param name phone, log, contacts, fav
        """
        scroll('up', 2)
        time.sleep(1)
        if name == "phone":
            scroll('left', 3)
        elif name == "contacts":
            scroll('right', 4)
            scroll('left', 1)
        elif name == "fav":
            scroll('right', 4)
        else:
            scroll('left', 4)
            scroll('right',1 )
        time.sleep(1)

    def add(self, contact, options=["done"]):  
        """ Add contact """  
        self.screen("contacts")
        menu()
        # click add contact
        scroll('up', 2)
        time.sleep(1)
        scroll('right')
        time.sleep(1)
        enter()
        time.sleep(1)

        # add given name
        scroll('up', 7)
        scroll('down')
        enter(contact.getFirstname())
        scroll('down')
        time.sleep(1)

        # add family name
        enter(contact.getLastname())
        scroll('down', 2)
        time.sleep(1)

        # add phone
        enter(contact.getPhone())
        scroll('down', 2)
        time.sleep(1)
      
        # add email
        enter(contact.getEmail())
        time.sleep(1)
        
        scroll('down', 7)
        time.sleep(1)
        scroll('right')
        # save or revert contact
        if options[0] == 'revert':
            scroll('right')
        else:
            scroll('left')
        enter()
        time.sleep(3)


    def find(self, term):
        self.screen("contacts")
        menu()
        time.sleep(1)
        # click search
        scroll('up', 2)
        enter()
        time.sleep(1)

        # enter search term 
        enter(term)
        enter()
        time.sleep(2)

        # select contact
        scroll('down')

        # open contact
        enter()
        time.sleep(2)
        enter()
        time.sleep(2)


    def delete(self):
        """ assumes you are in call screen """
        menu()
        time.sleep(1)

        # click delete contact
        scroll('down', 2)
        time.sleep(1)
        scroll('right', 1)
        time.sleep(1)
        enter()
        time.sleep(1)

        # click Yes on delete prompt
        enter() 
        time.sleep(2)

        # go back to main screen
        back()
        time.sleep(1)
        back()
        time.sleep(1)
