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

import unittest
import testlib
import imagelib
import applib
import os


class AddContactDemoTest(unittest.TestCase):
    """
        Add contact test for demo with only 1 test.
    """

    device = testlib.testenv.getDeviceClass()
    lastname = 'Regression'
    phone = '6501234567'
    email = 'test6509876543@t.co.uk'
    contact = applib.Contact()

    def setUp(self):
        self.log = self.device.initLogger(self._testMethodName, \
            self.__class__.__name__)
        self.log.info('Start')
        self.contact.clearAll()
        self.firstname = self._testMethodName
        self.contact.setFirstname(self.firstname)
        self.contact.setLastname(self.lastname)


    def testAddPhoneEmail(self):
        # Test customer create
        self.contact.setPhone(self.phone)
        self.contact.setEmail(self.email)
        self.log.info(self.contact)
        self.device.add(self.contact)


    def tearDown(self):
        # Search and delete contact  
        self.log.info('Search and delete contact...')
        self.device.find(self.firstname)
        self.validate()
        self.device.delete()
        self.log.info('Finished')


    def validate(self, testname=None):
        """Verify that add contact succeed by viewing contact details"""
        self.assertTrue(imagelib.compare(self.device, self.firstname, "+0+10%", 1000))



if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestSuite()
    unittest.TextTestRunner(verbosity=2).run(suite)
