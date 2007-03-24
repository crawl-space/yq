# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Pop(command.Command):
    summary = "pop a transaction off the stack"
    description = """This command will pop the most recently applied transaction off the stack. All changes to your system will be reversed."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        from yq import stack
        from yq.backend import yumbackend

        transaction_name = stack.top()
        yumbackend.pop(transaction_name)

        #Remove from the series
        #yes, this will eat files and babies
        status = open(config.STATUS, 'r')
        lines = status.readlines()
        status.close()
        status = open(config.STATUS, 'w')
        for line in lines[:-1]:
            status.write(line)
        status.close()
