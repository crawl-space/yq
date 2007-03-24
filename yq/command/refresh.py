# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Refresh(command.Command):
    summary = "refresh the current transaction"
    description = """This command will refresh the currently applied transaction to include all recent changes to your system."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import difflib
        import os
        from yq.backend import yumbackend

        current_pkgs = yumbackend.list_installed()

        base = open(config.BASE, 'r')
        base_pkgs = base.readlines()

        status = open(config.STATUS, 'r')
        status_lines = status.readlines()
        for line in status_lines[:-1]:
            transaction_name = line.strip()
            transaction = open(os.path.join(config.STACKDIR, transaction_name),
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
        transaction = open(os.path.join(config.STACKDIR, transaction_name),
                'w')

        d = difflib.Differ()
        for line in d.compare(base_pkgs, current_pkgs):
            if line[0] in ('-', '+'):
                transaction.write(line)

        base.close()
        transaction.close()
