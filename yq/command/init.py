# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Init(command.Command):
    summary = "initialize the yq data"
    description = """This command will create the files and directories needed by yq."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        pass
