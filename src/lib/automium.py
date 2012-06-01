#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Automium System
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Automium System.
#
# Hive Automium System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Automium System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Automium System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 9712 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-08-10 13:42:37 +0100 (ter, 10 Ago 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import time
import json
import sched
import shutil
import getopt
import datetime
import subprocess

LOOP_TIME = 20
""" The default time to be used in between iteration
of the build automation process (delay time) """

VERSION = "0.1.0"
""" The version value """

RELEASE = "120"
""" The release value """

BUILD = "1"
""" The build value """

RELEASE_DATE = "23 April 2002"
""" The release date value """

BRANDING_TEXT = "Hive Automium System %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

DEBUG = True
""" The current verbose level control, in case this flag
is set there will be much more information in the output """

def information():
    # print the branding information text and then displays
    # the python specific information in the screen
    print(BRANDING_TEXT % (VERSION, RELEASE, BUILD, RELEASE_DATE))
    print(VERSION_PRE_TEXT + sys.version)

def run(configuration):
    # retrieves the series of configuration values used
    # in the running, defaulting to the pre defined values
    # in case they are not defined
    run_name = configuration.get("name", "Configuration File")
    name = configuration.get("file", "build.bat")

    # prints the command line information
    print("------------------------------------------------------------------------")
    print("Building '%s'..." % run_name)

    # retrieves the current timestamp and then converts
    # it into the default integer "view"
    timestamp = time.time()
    timestamp = int(timestamp)

    # sets the appropriate build execution file name an
    # the shell execution flag according to the currently
    # executing operative system
    if os.name == "nt": name = "build.bat"; shell = False
    else: name = "build.sh"; shell = True

    # retrieves the current working directory and then uses
    # it to (compute) the complete file name
    current = os.getcwd()
    name = os.path.join(current, name)

    # in case the script file to be executed does not exists
    # in the current path raises an exception
    if not os.path.exists(name): raise RuntimeError("build script '%s' not found" % name)

    # in case the temporary directory does not exists creates
    # it then changes the current working directory to that
    # same temporary directory (files to be created there)
    not os.path.exists("tmp") and os.makedirs("tmp")
    os.chdir("tmp")

    try:
        # opens the file that will be used for the logging of
        # the operation
        log_file = open("automium.log", "wb")

        try:
            # runs the default build operation command, this should
            # trigger the build automation process, retrieves the
            # return value that should represent the success
            return_value = subprocess.call(name, stdin = None, stdout = log_file, stderr = log_file, shell = shell)
        finally:
            # closes the file immediately to avoid any file control
            # leaking (could cause memory leak problems)
            log_file.close()
    finally:
        # changes the current directory to the original position
        # this should be able to avoid path problems
        os.chdir(current)

    # creates the directory(s) used for the log and then moves
    # the log file into it (final target place)
    not os.path.exists("tmp/build/log") and os.makedirs("tmp/build/log")
    shutil.move("tmp/automium.log", "tmp/build/log/automium.log")

    # creates the directory(s) used for the various builds and then
    # moves the resulting contents into the correct target build
    # directory for the current build
    not os.path.exists("builds") and os.makedirs("builds")
    shutil.move("tmp/build", "builds/build_%d" % timestamp)

    # removes the temporary directory (avoids problems with
    # leaking file from execution)
    shutil.rmtree("tmp")

    # retrieves the (final) timestamp then converts it into the
    # default integer base value and then calculates the delta values
    timestamp_f = time.time()
    timestamp_f = int(timestamp_f)
    delta = timestamp_f - timestamp

    # retrieves the current date time information and
    # then formats it according to the value to be displayed
    now = datetime.datetime.now()
    now_string = now.strftime("%d/%m/%y %H:%M:%S")

    # retrieves the proper success string according to the
    # result from the batch file execution
    if return_value == 0: success = "SUCCEEDED"
    else: success = "FAILED"

    # prints the command line information
    print("Build finished and %s" % success)
    print("Files for the build stored at 'builds/build_%s'" % timestamp)
    print("Total time for build automation %d seconds" % delta)
    print("Finished build automation at %s" % now_string)

def cleanup():
    os.path.exists("tmp") and shutil.rmtree("tmp")

def schedule(configuration):
    # creates the scheduler object with the default
    # time and sleep functions (default behavior)
    scheduler = sched.scheduler(time.time, time.sleep)

    # iterates continuously for the loop on the scheduler
    # this will enter the new task into it and then run
    # the next scheduler task
    while True:
        # enters the run task into the scheduler and then
        # runs it properly
        scheduler.enter(LOOP_TIME, 1, run, (configuration,))
        scheduler.run()

def _set_default():
    if os.path.exists("build.bat"): sys.argv.insert(1, "build.json")
    else: raise RuntimeError("missing build file (invalid number of arguments)")

def main():
    # retrieves the number of arguments provided
    # to the the current execution script
    arg_count = len(sys.argv)
    if arg_count < 2 or not sys.argv[1].endswith(".json"): _set_default()

    # retrieves the path to the configuration file
    # to be used in the current execution
    file_path = sys.argv[1]
    file = open(file_path, "rb")
    try: configuration = json.load(file)
    finally: file.close()

    # displays the branding information on the screen so that
    # the user gets a feel of the product
    information();

    # sets the default variable values for the various options
    # to be received from the command line
    keep = False

    # parses the various options from the command line and then
    # iterates over the map of them top set the appropriate values
    # for the variables associated with the options
    options, _arguments = getopt.getopt(sys.argv[2:], "k", ["keep"])
    for option, _argument in options:
        if option in ("-k", "--keep"):
            keep = True

    # in case the keep flag value is set starts the process in
    # schedule mode otherwise runs "just" one iteration
    if keep: schedule(configuration)
    else: run(configuration)

def main_s():
    try: main()
    except: pass

if __name__ == "__main__":
    try: DEBUG and not main() or main_s()
    finally: cleanup()
