# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Push(command.Command):
    summary = "push a transaction onto the stack"
    description = """This command will push the next transaction onto the stack, modifing the system.""" 

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        from yq import stack
        from yq.backend import yumbackend

        transaction_name = stack.next()
        yumbackend.push(transaction_name)

        # add to the status
        status = open(config.STATUS, 'a')
        print >> status, transaction_name
        status.close()
