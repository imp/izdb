#
# Copyright 2014 Cyril Plisko. All rights reserved.
# Use is subject to license terms.
#
import ctypes as C

libzpoolfile = C.utils.find_library('libzpool')
__libzpool = C.CDLL(libzpoolfile)


