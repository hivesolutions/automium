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
import time
import sched
import shutil
import subprocess

LOOP_TIME = 10
""" The default time to be used in between iteration
of the build automation process (delay time) """

def run():
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

    # opens the file that will be used for the logging of
    # the operation
    log_file = open("automium.log", "wb")

    try:
        # runs the default build operation command, this should
        # trigger the build automation process
        subprocess.call(name, stdout = log_file, stderr = log_file, shell = shell)
    finally:
        # closes the file immediately to avoid any file control
        # leaking (could cause memory leak problems)
        log_file.close()

    # creates the directory(s) used for the log and then moves
    # the log file into it (final target place)
    os.makedirs("build/log")
    shutil.move("automium.log", "build/log/automium.log")

    # creates the directory(s) used for the various builds and then
    # moves the resulting contents into the correct target build
    # directory for the current build
    os.makedirs("builds")
    shutil.move("build", "builds/build_%d" % timestamp)

def main():
    print("Starting Hive Automium System ...")

    # creates the scheduler object with the default
    # time and sleep functions (default behavior)
    scheduler = sched.scheduler(time.time, time.sleep)

    # iterates continuously for the loop on the scheduler
    # this will enter the new task into it and then run
    # the next scheduler task
    while True:
        # enters the run task into the scheduler and then
        # runs it properly
        scheduler.enter(LOOP_TIME, 1, run, ())
        scheduler.run()

if __name__ == "__main__":
    main()
