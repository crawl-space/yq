# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Show(command.Command):
    summary = "print the changes in a transaction"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import os
 
        top_transaction = None
        status = open("/var/lib/yq/status", 'r')
        for line in status:
            top_transaction = line
        status.close()

        if not top_transaction:
            print "no applied transactions"    
        else:
            transaction = open(os.path.join("/var/lib/yq/",
                top_transaction.strip()), 'r')

            for line in transaction:
                line = line.strip()
                print line
