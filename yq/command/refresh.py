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
            current_pkgs.append("%s %s %s %s %s\n" %
                    (pkg['name'], pkg['epoch'], pkg['version'], pkg['release'],
                        pkg['arch']))

        base = open("/var/lib/yq/base", 'r')
        base_pkgs = base.readlines()

        status = open("/var/lib/yq/status", 'r')
        status_lines = status.readlines()
        for line in status_lines[:-1]:
            transaction_name = line.strip()
            transaction = open(os.path.join("/var/lib/yq/", transaction_name),
                    'r')
            for change in transaction:
                if change[0] == '-':
                    base_pkgs.remove(change[2:])
                elif change[0] == '+':
                    base_pkgs.append(change[2:])
                else:
                    assert False, "bad transaction file"
        
        base_pkgs.sort() 
        current_pkgs.sort() 
        
        transaction_name = status_lines[-1].strip()
        transaction = open(os.path.join("/var/lib/yq/", transaction_name), 'w')

        d = difflib.Differ()
        for line in d.compare(base_pkgs, current_pkgs):
            if line[0] in ('-', '+'):
                transaction.write(line)

        base.close()
        transaction.close()
