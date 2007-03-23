# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class New(command.Command):
    summary = "create a new transaction"
    usage = "new TRANSACTION"
    description = """This command will create a new transaction for tracking package changes."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import os

        if len(args) != 1:
            self.stderr.write("no transaction name given\n")
            return 1

        transaction = args[0]

        series = open(config.SERIES, 'a')
        print >> series, transaction
        series.close()

        status = open(config.STATUS, 'a')
        print >> status, transaction
        status.close()

        transaction_file = open(config.STACKDIR, transaction, 'w')
        transaction_file.close()
