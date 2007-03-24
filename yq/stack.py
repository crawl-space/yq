# vi:si:et:sw=4:sts=4:ts=4

from yq.util import config


def top():
    status = open(config.STATUS, 'r')
    for line in status: pass
    status.close()
    transaction_name = line.strip()
    return transaction_name
