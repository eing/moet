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

    def getScreenShot(self, file):
        screenshot(file)

    def launch(self):
        """ Launch app """
        touch(128,388)

    def screen(self, name="phone"):
        """ Navigate to different screens
            @param name phone, log, contacts, fav
        """
        if name == "phone":
            touch(17,44)
        elif name == "contacts":
            touch(210, 53)
        elif name == "fav":
            touch(277, 52)
        else:
            touch(140, 49)

    def phone(self, phone, options="[end]"):
        """ Phone activity
            @param phone phone number to dial
            @param options list of activities after call is placed
        """
        phone = str(phone)
        self.screen("phone")
        phonelen = len(phone)
        index = 0 
        while index < phonelen:
            dialnum = phone[index]
            if dialnum == '1':  
                touch(81,209)
            elif dialnum == '2':  
                touch(140,208)
            elif dialnum == '3':  
                touch(239,198)
            elif dialnum == '4':  
                touch(53,261)
            elif dialnum == '5':  
                touch(166,266)
            elif dialnum == '6':  
                touch(242,274)
            elif dialnum == '7':  
                touch(33,329)
            elif dialnum == '8':  
                touch(147,322)
            elif dialnum == '9':  
                touch(245,327)
            elif dialnum == '0':  
                touch(147,383)
            index = index + 1
            
        # dial  
        touch(125,467)
        time.sleep(2)
        
        # end call
        self.endcall()

    def endcall(self):
        """ assumes you are in contact detail screen """
        menu()
        time.sleep(1)
        touch(275,391)


    def add(self, contact, options=["done"]):  
        """ Add contact """  
        self.screen("contacts")
        menu()
        # click add contact
        touch(242,375)
        time.sleep(1)

        # add given name
        scroll('up')
        scroll('up')
        scroll('down')
        enter(contact.getFirstname())
        scroll('down')
        time.sleep(1)

        # add family name
        enter(contact.getLastname())
        scroll('down')
        scroll('down')
        time.sleep(1)

        # add phone
        enter(contact.getPhone())
        scroll('down')
        scroll('down')
        time.sleep(1)
      
        # add email
        enter(contact.getEmail())
        time.sleep(1)
        
        # save or revert contact
        if options[0] == 'revert':
            touch(211,453)
        else:
            touch(94,462)
        time.sleep(3)


    def find(self, term):
        self.screen("contacts")
        menu()
        time.sleep(1)
        # click search
        touch(60,361)
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
        touch(265,437)
        time.sleep(1)

        # click Yes on delete prompt
        touch(89,301)
        time.sleep(2)

        # go back to main screen
        back()
        time.sleep(1)
        back()
        time.sleep(1)
