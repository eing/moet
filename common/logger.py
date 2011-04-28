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

""" Common logging utility """

__version__ = '1.0'
__license__ = "EPL 1"
__author__ = [ 'Eing Ong @eingong' ]

import os
import logging


try:
    import testlib
    testoutput = testlib.settings.testoutput
except:
    testoutput = ''
    

# Logs go to util.log if no filename is specified
LOG_FILENAME = os.path.join(testoutput, 'util.log')

def getLogger(classname=None, logfile=LOG_FILENAME):
    """ 
        Initialize logging configuration. 
        Log file : $TEST_OUTPUT/util.log (default)
        Log levels : $LOG_LEVEL - ERROR||DEBUG||INFO||WARNING||CRITICAL
    """

    # If user specifies a logfile, use it!
    if logfile <> LOG_FILENAME:
        if logfile <> None:
            logfile = os.path.join(testoutput, logfile + '.log')

    # Create log dir if it does not exist
    if not os.path.exists(testoutput):
        os.makedirs(testoutput)

    # Create file if it does not exist
    if not os.path.exists(logfile):
        logfileIO = open(logfile, 'a')
        logfileIO.close() 

    logger = logging.getLogger(classname)

    fileHandler = logging.FileHandler(logfile) 
    formatter = logging.Formatter(\
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    logLevel = os.getenv('LOG_LEVEL')
    if not(logLevel):
        logger.setLevel(logging.ERROR)
    elif logLevel == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif logLevel == 'INFO':
        logger.setLevel(logging.INFO)
    elif logLevel == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif logLevel == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.ERROR)
    return logger


if __name__ == "__main__":
    log = getLogger('test', 'test')
    log.error('testing error logging')
    log.debug('testing debug logging')
    log.info('testing info logging')

    log1 = getLogger(None, 'runlog')
    log1.warning('testing warning logging')
    log1.critical('testing critical logging')
