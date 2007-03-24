# vi:si:et:sw=4:sts=4:ts=4

from yq.util import config


def top():
    top = None
    status = open(config.STATUS, 'r')
    for line in status:
        top = line
    if top:
        top = top.strip()
    return top
