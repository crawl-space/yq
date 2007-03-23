# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Top(command.Command):
    summary = "print the name of the current transaction"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        transaction = None
        status = open(config.STATUS, 'r')
        for line in status:
            transaction = line
        if transaction:
            print transaction.strip()
        else:
            print "no transactions on the stack"
