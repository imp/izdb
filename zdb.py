#
# Copyright 2014 Cyril Plisko. All rights reserved.
# Use is subject to license terms.
#

from __future__ import print_function
import libzpool


class Zdb(object):
    def __init__(self, arc_max, arc_meta_limit):
        super(Zdb, self).__init__()
        self.debug = False
        self.readonly = True
        self.zfs_arc_max = arc_max
        self.zfs_arc_meta_limit = arc_meta_limit

    def zdb_init(self):
        libzpool.kernel_init(libzpool.FREAD)
        libzpool.zfs_arc_max = self.zfs_arc_max
        libzpool.zfs_arc_meta_limit = self.zfs_arc_meta_limit

    def zdb_fini(self):
        libzpool.kernel_fini()
