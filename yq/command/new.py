# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

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

        series = open("/var/lib/yq/series", 'a')
        print >> series, transaction
        series.close()

        status = open("/var/lib/yq/status", 'a')
        print >> status, transaction
        status.close()

        transaction_file = open(os.path.join("/var/lib/yq/", transaction), 'w')
        transaction_file.close()
