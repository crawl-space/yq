# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Refresh(command.Command):
    summary = "refresh the current transaction"
    description = """This command will refresh the currently applied transaction to include all recent changes to your system."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import difflib
        import os
        import rpm

        ts = rpm.TransactionSet()
        mi = ts.dbMatch()

        current_pkgs = []
        for pkg in mi:
            current_pkgs.append("%s %s %s %s %s\n" % (pkg['name'], pkg['epoch'], pkg['version'], pkg['release'], pkg['arch']))

        base = open("/var/lib/yq/base", 'r')
        base_pkgs = base.readlines()

        series = open("/var/lib/yq/status", 'r')
        for line in series: pass
        transaction_name = line.strip()
        transaction = open(os.path.join("/var/lib/yq/", transaction_name), 'w')

        d = difflib.Differ()
        for line in d.compare(base_pkgs, current_pkgs):
            if line[0] in ('-', '+'):
                transaction.write(line)

        base.close()
        transaction.close()
