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
    Useful classes and functions for the app i.e. Contact Manager
    using OO concepts.
"""

class Contact:
    """ Representation of contact"""

    def __init__(self):
        """Default settings for contact"""
        self.clearAll()


    def __str__(self):
        """Return contact string"""
        space = ' '
        newline = ' \n '
        return newline + '[Name] ' + self.firstname + space + self.lastname \
            + newline + '[Phone] ' + self.phone \
            + newline + '[Email] ' + self.email 

    def clearAll(self):
        """Set all attributes to empty strings or default values"""
        self.firstname = ''
        self.lastname = ''
        self.phone = ''
        self.email = ''

    def setFirstname(self, firstname):
        """Set firstname"""
        self.firstname = firstname
        
    def getFirstname(self):
        """Returns contact firstname"""
        return self.firstname
        
    def setLastname(self, lastname):
        """Set lastname"""
        self.lastname = lastname
        
    def getLastname(self):
        """Returns contact lastname"""
        return self.lastname
        
    def setPhone(self, phone):
        """Set phone"""
        self.phone = phone

    def getPhone(self):
        """Returns contact phone"""
        return self.phone

    def setEmail(self, email):
        """Set email"""
        self.email = email

    def getEmail(self):
        """Returns contact email"""
        return self.email
