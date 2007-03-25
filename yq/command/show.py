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
        from yq import stack

        if len(args) == 0:
            transaction_name = stack.top()

            if not transaction_name:
                self.stdout.write("no applied transactions\n")
                return 0
        else:
            transaction_name = args[0]

        transaction = open(os.path.join(config.STACKDIR, transaction_name),
                'r')
        self.stdout.writelines(transaction)
