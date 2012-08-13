#!/bin/sh

export MOET=$HOME/sandbox/ifs/qa/moet
export MOBILETEST=$HOME/sandbox/ifs/qa/AddressBookTest
export ANDROID_HOME=/Users/eong/sandbox/android-sdk-macosx

export PATH=.:$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$MOET/src

export CLASSPATH=$MOET/bin/resources/junit.jar:$JAVA_HOME/bundle/Classes/classes.jar:$JAVA_HOME/bundle/Classes/ui.jar:$MOBILETEST/bin:$MOET/bin:$MOET/bin/resources/android.jar:$MOET/bin/resources/androidprefs.jar:$MOET/bin/resources/commons-compress-1.0.jar:$MOET/bin/resources/ddmlib.jar:$MOET/bin/resources/guavalib.jar:$MOET/bin/resources/hamcrest.jar:$MOET/bin/resources/jython.jar:$MOET/bin/resources/monkeyrunner.jar:$MOET/bin/resources/sdklib.jar:$MOET/bin/resources/sikuli-script.jar:$CLASSPATH

echo $PATH
pushd /Users/eong/sandbox/eclipse/Eclipse.app/Contents/MacOS
exec "`dirname \"$0\"`/eclipse" $@
