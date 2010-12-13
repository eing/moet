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
import testlib
import logger

class AppInterface:
    """ Application interface for all devices to implement """

    # Environment variables
    testenv = testlib.testenv
    testroot = testenv.testroot
    testoutput = testenv.testoutput
    device = testenv.device

    def initLogger(self, testname='AddressBook', logfile=None):
        """ Initialize logger for all tests """
        self.log = logger.getLogger(testname, logfile)
        return self.log

    def launch(self):
        """ Launch application"""
        print "Launching app"

    def add(self, contact, options='save'):
        """ Add contact """  
        print "Adding contact"

    def find(self, contact=None, options=None):
        """ Find contact """
        print "Finding contact"

    def delete(self, execute=True):
        """ Delete loaded contact """
        print "Deleting contact"
