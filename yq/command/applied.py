# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Applied(command.Command):
    summary = "print all transactions on the stack"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        transaction = None
        status = open("/var/lib/yq/status", 'r')
        for line in status:
            transaction = line
            print transaction.strip()
        if not transaction:
            print "no transactions on the stack"
