# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Show(command.Command):
    summary = "print the changes in a transaction"
    usage = "show [TRANSACTION]"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import os

        if len(args) == 0:
            top_transaction = None
            status = open(config.STATUS, 'r')
            for line in status:
                top_transaction = line
            status.close()

            if not top_transaction:
                print "no applied transactions"
                return 0
            else:
                transaction_name = top_transaction.strip()
        else:
            transaction_name = args[0]

        transaction = open(os.path.join(config.STACKDIR, transaction_name),
                'r')

        for line in transaction:
            line = line.strip()
            print line
