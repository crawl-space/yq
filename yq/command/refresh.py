# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Refresh(command.Command):
    summary = "refresh the current transaction"
    description = """This command will refresh the currently applied transaction to include all recent changes to your system."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        pass
