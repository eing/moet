#
# Copyright 2010 Intuit, Inc.
#
# Licensed under the Eclipse Public License, Version 1.0 (the "License"); you may
# not use this file except in compliance with the License. Please see the License 
# for the specific language governing permissions and limitations.
# You may obtain a copy of the License at
#
# http://www.eclipse.org/legal/epl-v10.html
#

"""
   Utility for androidlib.py. 
   Translates an list of adb getevents to adb sendevent for playback
   E.g.
      Input  : /dev/input/event0: 0001 00e5 00000001
      Output : sendevent /dev/input/event0 1 229 1
"""

def translate(inputString):
    colonSplit = inputString.split(':')
    if len(colonSplit) < 2:
        return ''
    spaceSplit = colonSplit[1].split()
    if len(spaceSplit) < 3:
        return ''
    base = 16
    command = 'sendevent ' 

    deviceList = colonSplit[0].split('/')
    device = '/' + deviceList[1] + '/' + deviceList[2]  + '/' + deviceList[3] \
        +  ' '
    type = str(int(spaceSplit[0], base)) + ' '
    code = int(spaceSplit[1], base)
    value = str(int(spaceSplit[2], base))

    code = str(code) + ' '
    outputString = command + device + type + code + value
    return outputString
    
if __name__ == "__main__":

    print 'Enter adb getevents > ' 
    notDone = True
    translateList = list()

    while notDone:
        translateList.append(raw_input())
        if '#' in translateList:
            notDone = False

    size = len(translateList) - 1
    index = 0
    outputString = ''
    print '[Command] [Device] [Type] [Code] [Value]'
    while index < size:
        outputString = outputString + translate(translateList[index]) + '\n'
        index = index + 1

    print outputString
