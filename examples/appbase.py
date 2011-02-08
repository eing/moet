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

class AppInterface:
    """ Application interface for all devices to implement """

    def initLogger(self, testname='AddressBook', logfile=None):
        """ Initialize logger for all tests """
        try:
            import testlib
            import logger
            testenv = testlib.testenv
            testroot = testenv.testroot
            testoutput = testenv.testoutput
            device = testenv.device
            self.log = logger.getLogger(testname, logfile)
        except:
            # Create app.log with DEBUG log level
            logfile="app.log"
            if not os.path.exists(logfile):
                logfileIO = open(logfile, 'a')
                logfileIO.close()
            self.log = logging.getLogger(logfile)
            fileHandler = logging.FileHandler(logfile)
            formatter = logging.Formatter(\
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            fileHandler.setFormatter(formatter)
            self.log.addHandler(fileHandler)
            self.log.setLevel(logging.DEBUG)
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
