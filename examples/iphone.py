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

from iphonelib import *
import os
import time
import applib
import appbase

class iPhoneImpl(appbase.AppInterface):
    """
        IPhone implementation of methods specified in interface class.
    """

    def getScreenShot(self, file='test'):
        """ Takes screenshot of current device
            @param file filename with no extension as file will be named file
        """
        screenshot(file)

    def launch(self):
        """ Launch app with activity and component name """
        touchImage('IconContacts')

    def add(self, contact, options=["done"]):  
        """ Add contact """  
        # touchImage add contact
        touchImage('ButtonAddContact')
        time.sleep(1)

        # add given name
        touchImage('EntryFirstname')
        enter(contact.getFirstname())
        time.sleep(1)

        # add family name
        touchImage('EntryLastname')
        enter(contact.getLastname())
        time.sleep(1)

        # add phone
        touchImage('EntryMobile')
        enter(contact.getPhone())
        time.sleep(1)
      
        # add email
        scroll('down', 3)
        touchImage('EntryEmail')
        enter(contact.getEmail())
        time.sleep(1)
        
        # save or cancel
        if options[0] == 'cancel':
            touchImage('KeyCancel')
        else:
            touchImage('KeyDone')
        time.sleep(2)

        # Back to main screen
        touchImage('ButtonAllContacts')
        time.sleep(1)


    def find(self, term):
        # touchImage search
        touchImage('EntrySearch')
        time.sleep(1)
        # enter search term 
        enter(term)

        # select contact
        touchImage('IconMoreDetails')
        time.sleep(3)


    def delete(self):
        """ assumes you are in call screen """
        touchImage('KeyEdit')
        time.sleep(1)

        # display delete contact
        scroll('down', 3)

        # touchImage delete contact
        touchImage('ButtonDeleteContact')
        time.sleep(1)

        # Confirm delete  on delete prompt
        touchImage('ButtonDeleteContactConfirm')
        time.sleep(1)

        # Back to main screen
        touchImage('KeyCancel')
        time.sleep(1)
