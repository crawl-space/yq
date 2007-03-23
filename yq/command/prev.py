# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Prev(command.Command):
    summary = "print the name of the previous transaction on the stack"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        transaction = None
        status = open(config.STATUS, 'r')
        transaction = status.readline()
        if not transaction:
            print "no transactions on the stack"
        else:
            prev_transaction = None
            for line in status:
                prev_transaction = transaction
                transaction = line
            if prev_transaction:
                print prev_transaction.strip()
            else:
                print "only one transaction on the stack"
