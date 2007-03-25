# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Help(command.Command):
    summary = "show help"
    usage = "help [COMMAND]"

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        if len(args) == 0:
            self.parentCommand.parser.print_help()
        elif len(args) == 1:
            command = args[0]
            parent = self.parentCommand
            if command in parent.subCommands.keys():
                parent.subCommands[command].parser.print_help()
            elif parent.aliasedSubCommands:
                if command in parent.aliasedSubCommands.keys():
                    parent.aliasedSubCommands[command].parser.print_help()
            else:
                self.stdout.write("unknown command '%s'\n" % command)
