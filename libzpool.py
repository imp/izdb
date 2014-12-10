#
# Copyright 2014 Cyril Plisko. All rights reserved.
# Use is subject to license terms.
#
from ctypes.util import find_library
import ctypes as C

FREAD = 1
FWRITE = 2

libzpoolfile = find_library('zpool')
__libzpool = C.CDLL(libzpoolfile)

spa_config_path = C.c_char_p.in_dll(__libzpool, 'spa_config_path')
zfs_arc_max = C.c_long.in_dll(__libzpool, 'zfs_arc_max')

kernel_init = __libzpool.kernel_init
kernel_init.argtypes = [C.c_int]
kernel_init.restype = None

kernel_fini = __libzpool.kernel_fini
kernel_fini.argtypes = None
kernel_fini.restype = None
