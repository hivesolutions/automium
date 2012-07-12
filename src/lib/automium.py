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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import stat
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

RECURSION = (0, 0, 0, LOOP_TIME, 0)
""" The default recursion list to be used for the
control of the iteration process """

TIMESTAMP_PRECISION = 100.0
""" The precision to be used for the timestamp integer
identifier calculation (more precision less collisions) """

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

OS_ALIAS = {
    "nt" : "win32",
    "posix" : "unix"
}
""" Map defining the various alias to the operative system
names based on the python definition of the names """

def delta_string(delta, counts = 2):
    # starts the counter value (number of elements
    # and the valid flag)
    counter = 0
    valid = False

    # starts the initial buffer string as
    # an empty string (no delta value)
    buffer = ""

    # calculates the delta resulting value for the
    # number of days in the delta in case this value
    # is greater than zero it must be processed
    value = delta / 86400
    if value > 0:
        # retrieves the appropriate format string according
        # to the resulting value
        if value == 1: format = "%d day "
        else: format = "%d days "

        # formats the value using the format string and the
        # resulting value and then update the value of the
        # counter and sets the valid flag
        buffer += format % value
        counter += 1
        valid = True

    # checks if the current counter reached the count limit
    # in such case returns the current buffer stripped
    if counter == counts: return buffer.rstrip()

    # calculates the delta resulting value for the
    # number of hours in the delta in case this value
    # is greater than zero it must be processed
    value = (delta % 86400) / 3600
    if valid or value > 0:
        # retrieves the appropriate format string according
        # to the resulting value
        if value == 1: format = "%d hour "
        else: format = "%d hours "

        # formats the value using the format string and the
        # resulting value and then update the value of the
        # counter and sets the valid flag
        buffer += format % value
        counter += 1
        valid = True

    # checks if the current counter reached the count limit
    # in such case returns the current buffer stripped
    if counter == counts: return buffer.rstrip()

    # calculates the delta resulting value for the
    # number of minutes in the delta in case this value
    # is greater than zero it must be processed
    value = (delta % 3600) / 60
    if valid or value > 0:
        # retrieves the appropriate format string according
        # to the resulting value
        if value == 1: format = "%d minute "
        else: format = "%d minutes "

        # formats the value using the format string and the
        # resulting value and then update the value of the
        # counter and sets the valid flag
        buffer += format % value
        counter += 1
        valid = True

    # checks if the current counter reached the count limit
    # in such case returns the current buffer stripped
    if counter == counts: return buffer.rstrip()

    # calculates the delta resulting value for the
    # number of seconds in the delta
    value = delta % 60

    # retrieves the appropriate format string according
    # to the resulting value
    if value == 1: format = "%d second "
    else: format = "%d seconds "

    # formats the value using the format string and the
    # resulting value and then update the value of the
    # counter and sets the valid flag
    buffer += format % value
    counter += 1
    valid = True

    # the end of execution has been reached so the buffer must
    # be stripped and returned
    return buffer.rstrip()

def byte_string(bytes):
    # sets the float value as the default option
    # for the byte string calculus
    is_float = True

    # calculates the giga byte integer value for the
    # currently provided set of bytes and it case
    # it's greater that zero proceed to calculus
    value = int(round(float(bytes) / 1073741824.0))
    if value > 0:
        # checks if the value is meant to be plural
        # and if it should be set as float value with
        # one decimal place (value to short)
        if value == 1: format = "%.1f GByte"
        elif value < 10: format = "%.1f GBytes"
        else: format = "%d GBytes"; is_float = True

        # converts the value into a decimal value in
        # case it's the case and formats it
        if is_float: value = float(bytes) / 1073741824.0
        return format % value

    # calculates the mega byte integer value for the
    # currently provided set of bytes and it case
    # it's greater that zero proceed to calculus
    value = int(round(float(bytes) / 1048576.0))
    if value > 0:
        # checks if the value is meant to be plural
        # and if it should be set as float value with
        # one decimal place (value to short)
        if value == 1: format = "%.1f MByte"
        elif value < 10: format = "%.1f MBytes"
        else: format = "%d MBytes"; is_float = True

        # converts the value into a decimal value in
        # case it's the case and formats it
        if is_float: value = float(bytes) / 1048576.0
        return format % value

    # calculates the kilo byte integer value for the
    # currently provided set of bytes and it case
    # it's greater that zero proceed to calculus
    value = int(round(float(bytes) / 1024.0))
    if value > 0:
        # checks if the value is meant to be plural
        # and if it should be set as float value with
        # one decimal place (value to short)
        if value == 1: format = "%.1f KByte"
        elif value < 10: format = "%.1f KBytes"
        else: format = "%d KBytes"; is_float = True

        # converts the value into a decimal value in
        # case it's the case and formats it
        if is_float: value = float(bytes) / 1024.0
        return format % value

    # calculates the byte integer value for the
    # currently provided set of bytes and it case
    # it's greater that zero proceed to calculus
    value = bytes
    if value > 0:
        # checks if the value is meant to be plural
        # and if it should be set as float value with
        # one decimal place (value to short)
        if value == 1: format = "%.1f Byte"
        elif value < 10: format = "%.1f Bytes"
        else: format = "%d Bytes"; is_float = True

        # converts the value into a decimal value in
        # case it's the case and formats it
        if is_float: value = float(bytes)
        return format % value

    # returns the default and only option left
    # as the zero bytes case
    return "0 Bytes"

def information():
    # print the branding information text and then displays
    # the python specific information in the screen
    print(BRANDING_TEXT % (VERSION, RELEASE, BUILD, RELEASE_DATE))
    print(VERSION_PRE_TEXT + sys.version)

def resolve_os():
    # retrieves the current specific operative system
    # name and then resolves it using the alias map
    os_name = os.name
    os_name = OS_ALIAS.get(os_name, os_name)
    return os_name

def resolve_file(files):
    # resolves the current operative system descriptive
    # name so that it's possible to correctly resolve
    # the correct file to be used
    os_name = resolve_os()

    # tries to retrieve the appropriate execution
    # file using both the "exact" operative system
    # name or in case it fails the wildcard based
    # operative system name , then returns it to the
    # caller method for execution
    file = files.get(os_name, None) or files.get("*", None)
    return file

def get_size(path):
    # sets the initial value for the total path
    # size (start at the initial value)
    total_size = 0

    # walks through the path to count the bytes in
    # each element
    for directory_path, _names, file_names in os.walk(path):
        # iterate over all the file names in the current
        # directory to count their size and "join" their
        # size to the current accumulator
        for file_name in file_names:
            file_path = os.path.join(directory_path, file_name)
            total_size += os.path.getsize(file_path)

    # returns the accumulator value containing the complete
    # set of byte count
    return total_size

def run(path, configuration, current = None):
    # retrieves the series of configuration values used
    # in the running, defaulting to the pre defined values
    # in case they are not defined
    run_name = configuration.get("name", "Configuration File")
    files = configuration.get("files", {"*" : "build.bat"})

    # resolves the "correct" file path from the provided
    # files map, this is done using the current os name
    file = resolve_file(files)

    # calculates the new execution directory (to be set
    # in the correct position) and then changed into it
    file_path = os.path.join(path, file)

    # sets the executing name as the file path resolved
    # this is the script to be executed
    name = file_path

    # prints the command line information
    print("------------------------------------------------------------------------")
    print("Building '%s'..." % run_name)

    # retrieves the current timestamp and then converts
    # it into the default integer "view" note that an
    # extra precision timestamp is also created for the
    # purpose of being used as the build identifier
    timestamp = time.time()
    timestamp_s = int(timestamp)
    timestamp_p = int(timestamp * TIMESTAMP_PRECISION)

    # sets the appropriate shell execution flag according
    # to the currently executing operative system
    if os.name == "nt": shell = False
    else: shell = True

    # retrieves the current working directory and then uses
    # it to (compute) the complete temporary path
    current = current or os.getcwd()
    tmp_path = os.path.join(current, "tmp")
    log_path = os.path.join(tmp_path, "automium.log")
    builds_path = os.path.join(current, "builds")
    build_path = os.path.join(builds_path, "%d" % timestamp_p)

    # in case the current path is not absolute (must) create
    # the complete path by joining the name with the current
    # path value (complete path construction)
    if not os.path.isabs(name) : name = os.path.join(current, name)

    # in case the script file to be executed does not exists
    # in the current path raises an exception
    if not os.path.exists(name): raise RuntimeError("build script '%s' not found" % name)

    # in case the temporary directory does not exists creates
    # it then changes the current working directory to that
    # same temporary directory (files to be created there)
    not os.path.exists(tmp_path) and os.makedirs(tmp_path)

    # checks the current permissions on the name of the file
    # to be executed (it must contain execution permission)
    # otherwise such permission must be added
    _stat = os.stat(name)
    _mode = _stat.st_mode
    if not _mode & stat.S_IXUSR: os.chmod(name, _mode | stat.S_IXUSR)

    # opens the file that will be used for the logging of
    # the operation
    log_file = open(log_path, "wb")

    try:
        # runs the default build operation command, this should
        # trigger the build automation process, retrieves the
        # return value that should represent the success
        process = subprocess.Popen([name], stdin = None, stdout = log_file, stderr = log_file, shell = shell, cwd = tmp_path)
        process.communicate()
        return_value = process.returncode
    finally:
        # closes the file immediately to avoid any file control
        # leaking (could cause memory leak problems)
        log_file.close()

    # creates the directory(s) used for the log and then moves
    # the log file into it (final target place)
    not os.path.exists(tmp_path + "/build/log") and os.makedirs(tmp_path + "/build/log")
    shutil.move(log_path, tmp_path + "/build/log/automium.log")

    # creates the directory(s) used for the various builds and then
    # moves the resulting contents into the correct target build
    # directory for the current build
    not os.path.exists(builds_path) and os.makedirs(builds_path)
    shutil.move(tmp_path + "/build", build_path)

    # removes the temporary directory (avoids problems with
    # leaking file from execution)
    shutil.rmtree(tmp_path)

    # retrieves the (final) timestamp then converts it into the
    # default integer base value and then calculates the delta values
    timestamp_f = time.time()
    timestamp_f = int(timestamp_f)
    delta = timestamp_f - timestamp_s

    # retrieves the current date time information and
    # then formats it according to the value to be displayed
    now = datetime.datetime.now()
    now_string = now.strftime("%d/%m/%y %H:%M:%S")

    # retrieves the proper success string according to the
    # result from the batch file execution
    if return_value == 0: success = "SUCCEEDED"
    else: success = "FAILED"

    # retrieves the name of the current operative system in
    # order to put it in the description
    os_name = resolve_os()

    # retrieves the total directory size for the build, this
    # is an interesting diagnostic metric
    size = get_size(build_path)
    size_string = byte_string(size)

    # calculate the string that describes the delta time in
    # an easy to understand value
    _delta_string = delta_string(delta)

    # creates the map that describes the current build
    # to be used to output this information into a descriptive
    # json file that may be interpreted by third parties
    description = {
        "id" : timestamp_p,
        "system" : os_name,
        "size" : size,
        "size_string" : size_string,
        "start_time" : timestamp_s,
        "end_time" : timestamp_f,
        "delta" : delta,
        "result" : return_value == 0
    }
    description_path = os.path.join(build_path, "description.json")
    description_file = open(description_path, "wb")
    try: json.dump(description, description_file)
    finally: description_file.close()

    # prints the command line information
    print("Build finished and %s" % success)
    print("Files for the build stored at 'builds/%s'" % timestamp_p)
    print("Total time for build automation %s" % _delta_string)
    print("Finished build automation at %s" % now_string)

def cleanup(current = None):
    # retrieves the current working directory and then uses
    # it to (compute) the complete temporary path, then in
    # case the temporary path exists removes it
    current = current or os.getcwd()
    tmp_path = os.path.join(current, "tmp")
    os.path.exists(tmp_path) and shutil.rmtree(tmp_path)

def schedule(path, configuration):
    # creates the scheduler object with the default
    # time and sleep functions (default behavior)
    scheduler = sched.scheduler(time.time, time.sleep)

    # tries to retrieve the recursion list from the configuration
    # in case it fails the default recursion list is used
    recursion = configuration.get("recursion", RECURSION)
    days, hours, minutes, seconds, miliseconds = recursion
    loop_time = days * 86400.0 + hours * 3600.0 + minutes * 60.0 + seconds + miliseconds / 1000.0

    # iterates continuously for the loop on the scheduler
    # this will enter the new task into it and then run
    # the next scheduler task
    while True:
        # enters the run task into the scheduler and then
        # runs it properly
        scheduler.enter(loop_time, 1, run, (configuration,))
        scheduler.run()

def _set_default():
    if os.path.exists("build.json"): sys.argv.insert(1, "build.json")
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
    information()

    # sets the default variable values for the various options
    # to be received from the command line
    keep = False

    # parses the various options from the command line and then
    # iterates over the map of them top set the appropriate values
    # for the variables associated with the options
    options, _arguments = getopt.getopt(sys.argv[2:], "k", ["keep"])
    for option, _argument in options:
        if option in ("-k", "--keep"): keep = True

    # "calculates" the base path for the execution of the various
    # scripts based on the current configuration file location
    path = os.path.dirname(file_path)

    # in case the keep flag value is set starts the process in
    # schedule mode otherwise runs "just" one iteration
    if keep: schedule(path, configuration)
    else: run(path, configuration)

def main_s():
    try: main()
    except: pass

if __name__ == "__main__":
    try: DEBUG and not main() or main_s()
    finally: cleanup()
