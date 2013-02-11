#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Automium System
# Copyright (C) 2008-2012 Hive Solutions Lda.
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
import hashlib

BUFFER_SIZE = 4096
""" The size of the buffer to be used when reading
from the file, should match a normal disk block """

class Hash:
    """
    Class that handles the hashing abstraction for
    a series of hashes and a given file.
    """

    def __init__(self, file_path, types):
        self.file_path = file_path
        self.types = types
        self.hashes = {}

        self._create()

    def update(self, data):
        for type in self.types:
            hash = self.hashes[type]
            hash.update(data)

    def dump_file(self):
        for type in self.types:
            # retrieves the hash for the current type in iteration
            # and uses it to compute the hexadecimal digest
            hash = self.hashes[type]
            digest = hash.hexdigest()

            # retrieves the "base" file name for the current file
            # path associated with the hash
            name = os.path.basename(self.file_path)

            # tries to retrieve the method to be used to retrieve the
            # format string for the current type and then calls it with
            # the current digest and name values
            method = getattr(self, "_" + type + "_format")
            format = method(digest, name)

            file = open(self.file_path + "." + type, "wb")
            try: file.write(format + "\n")
            finally: file.close()

    def _md5_format(self, digest, name):
        return "%s *%s" % (digest, name)

    def _sha256_format(self, digest, name):
        return "%s *%s" % (digest, name)

    def _create(self):
        for type in self.types:
            hash = hashlib.new(type)
            self.hashes[type] = hash

def hash_d(path, types = ("md5", "sha256")):
    """
    Computes the various hash values for the provided
    directory, the names of the generated files should
    conform with the base name for the file.

    @type path: String
    @param path: The path to the directory for which the
    hash values will be computed.
    @type types: Tuple
    @param types: The various types of hash digests to be
    generated for the various files in the directory.
    """

    # in case the provided path does not represents a valid
    # directory path (not possible to hash values) must raise
    # an exception indicating the problem
    if not os.path.isdir(path):
        raise RuntimeError("Invalid directory path '%s'" % path)

    # creates the map to be used to hold the various digest
    # values for the various types of hashes
    digests = {}

    # retrieves the various entries for the provided
    # directory path and iterates over them to create
    # the various hash value for them
    entries = os.listdir(path)
    for entry in entries:
        # constructs the complete path to the file to
        # be hashes and then opens it for reading
        file_path = os.path.join(path, entry)
        file = open(file_path, "rb")

        # creates the hash structure for the current file
        # and for the "selected" hash types
        hashes = Hash(file_path, types)

        try:
            # iterates continuously in order to be able to
            # read the complete data contents from the file
            # and update the hash accordingly
            while True:
                data = file.read(BUFFER_SIZE)
                if not data: break
                hashes.update(data)
        finally:
            # closes the file as it's not going to be used
            # anymore (avoids descriptor leaks)
            file.close()

        # dumps the file for the hashes structure (should
        # create the various files) and then stores the hashes
        # structure in the digest structure
        hashes.dump_file()
        digests[file_path] = hashes

hash_d("C:/repo_extra/viriatum/scripts/build/builds/136058106393/target/rabeton")
