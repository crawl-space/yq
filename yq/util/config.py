# vi:si:et:sw=4:sts=4:ts=4

import os

VERSION = '0.0.2'

STACKDIR = '/var/lib/yq'

BASE = os.path.join(STACKDIR, 'base')
SERIES = os.path.join(STACKDIR, 'series')
STATUS = os.path.join(STACKDIR, 'status')
