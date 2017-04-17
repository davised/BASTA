#!/usr/bin/env python

import sys
import os
import hashlib
import logging
import plyvel
import gzip
import timeit

############
#
#  Functions related to levelDB stuff
#
####
#   COPYRIGHT DISCALIMER:
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#   Author: Tim Kahlke, tim.kahlke@audiotax.is
#   Date:   April 2017
#


def create_db(path,f,of,i1,i2):

    logger = logging.getLogger()
    ip = os.path.join(path,f)
    op = os.path.join(path,of)

    lookup = plyvel.DB(op, create_if_missing=True)
    wb = lookup.write_batch()
    logger.info("#Reading mapping file\nThis might take a while, please be patient ...\n")

    timetotal = 0
    try:
        with gzip.open(ip,"r") as f:
            start_time = timeit.default_timer()
            for count,line in enumerate(f):
                if not count % 1000000:
                    if not count:
                        continue
                    elapsed = timeit.default_timer() - start_time
                    timetotal+=elapsed
                    num = count/1000000
                    logger.info("%d lines processed (avg time: %fsec)" % (count,timetotal/num))
                    start_time = timeit.default_timer()
                ls = line.split()
                lookup.put(ls[i1],ls[i2])
            lookup.close()
    except IOError:
        logger.error("No file %s: did you forget to download mapping file (parameter -d True)?" % (ip))


def _init_db(db):
        lookup = plyvel.DB(os.path.abspath(db))
        return lookup
