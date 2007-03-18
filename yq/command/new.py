# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class New(command.Command):
    summary = "create a new transaction"
    description = """This command will create a new transaction for tracking package changes."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        pass
