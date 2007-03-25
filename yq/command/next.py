# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Next(command.Command):
    summary = "print the name of the next transaction"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        from yq import stack
        transaction_name = stack.next()

        if not transaction_name:
            self.stdout.write("no unapplied transactions\n")
        else:
            self.stdout.write(transaction_name + '\n')
