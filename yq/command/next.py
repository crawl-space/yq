# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Next(command.Command):
    summary = "print the name of the next transaction"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        top_transaction = None
        status = open("/var/lib/yq/status", 'r')
        for line in status:
            top_transaction = line
        status.close()

        series = open("/var/lib/yq/series", 'r')
        if not top_transaction:
            transaction_name = series.readline().strip()
        else:
            line = series.readline()
            while line:
                if line == top_transaction:
                    transaction_name = series.readline().strip()
                    break
                line = series.readline()
            else:
                print "no unapplied transactions"
                return
        series.close()

        print transaction_name
