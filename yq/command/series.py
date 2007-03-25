# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Series(command.Command):
    summary = "print all transactions in the series"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        transaction = None
        series = open(config.SERIES, 'r')
        for line in series:
            transaction = line
            self.stdout.write(transaction)
        if not transaction:
            self.stdout.write("no transactions in the series\n")
