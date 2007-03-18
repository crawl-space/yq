# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Pop(command.Command):
    summary = "pop a transaction off the stack"
    description = """This command will pop the most recently applied transaction off the stack. All changes to your system will be reversed."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        pass
