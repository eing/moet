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
    Common exceptions library

"""

__version__ = '1.0'
__license__ = "EPL 1"
__author__ = [ 'Eing Ong @eingong' ]

class TestException(Exception):
    """ Base class for test exceptions """

    def __init__(self, ErrorMsg):
        self.ErrorMsg = ErrorMsg

    def __repr__(self):
        return repr('[' + self.ErrorCode + '] ' + self.ErrorMsg)
         
    def getErrorMessage(self):
        return self.ErrorMsg

    def getErrorCode(self):
        return self.ErrorCode


# Setup and Envirnoment Exceptions
class SetupException(TestException): ErrorCode = 100
class EnvironmentException(TestException): ErrorCode = 150
class OSSystemException(TestException): ErrorCode = 151

# Test Execution Exceptions
class TestExecutionException(TestException): ErrorCode = 200
class TestDataException(TestException): ErrorCode = 201
class ToolException(TestException): ErrorCode = 301

# Test Verification Exceptions
class TestVerificationException(TestException): ErrorCode = 400
class ImageVerificationException(TestException): ErrorCode = 402
class MissingImageFileException(TestException): ErrorCode = 403
