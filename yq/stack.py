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

def next():
    top_transaction = top()

    series = open(config.SERIES, 'r')
    if not top_transaction:
        transaction_name = series.readline().strip()
    else:
        transaction_name = None
        line = series.readline()
        while line:
            if line.strip() == top_transaction:
                transaction_name = series.readline().strip()
                break
            line = series.readline()
    series.close()

    return transaction_name
