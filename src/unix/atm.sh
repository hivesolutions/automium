#!/bin/sh
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

# __author__    = João Magalhães <joamag@hive.pt>
# __version__   = 1.0.0
# __revision__  = $LastChangedRevision: 9746 $
# __date__      = $LastChangedDate: 2010-08-12 14:07:04 +0100 (qui, 12 Ago 2010) $
# __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
# __license__   = GNU General Public License (GPL), Version 3

# sets the temporary variables
SCRIPT_NAME=automium.sh

# retrieves the script directory path
SCRIPT_DIRECTORY_PATH=$(dirname $(readlink -f $0))

# executes the "parent" script file that should
# exist in the current directory with the provided
# arguments (argument pipe)
"$SCRIPT_DIRECTORY_PATH/$SCRIPT_NAME" $*

# exits the process
exit $?