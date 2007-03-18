# -*- Mode: Python; test-case-name: testsuite.test_util_command -*-
# vi:si:et:sw=4:sts=4:ts=4

"""
Command class.

Originally from MOAP
https://apestaart.org/moap/trac/
"""

import optparse
import sys

class CommandHelpFormatter(optparse.IndentedHelpFormatter):
    """
    I format the description as usual, but add an overview of commands
    after it if there are any, formatted like the options.
    """
    _commands = None

    def addCommand(self, name, description):
        if self._commands is None:
            self._commands = {}
        self._commands[name] = description

    ### override parent method
    def format_description(self, description):
        ret = optparse.IndentedHelpFormatter.format_description(self,
            description)
        if self._commands:
            commandDesc = []
            commandDesc.append("commands:")
            keys = self._commands.keys()
            keys.sort()
            length = 0
            for key in keys:
                if len(key) > length:
                    length = len(key)
            for name in keys:
                format = "  %-" + "%d" % length + "s  %s"
                commandDesc.append(format % (name, self._commands[name]))
            ret += "\n" + "\n".join(commandDesc) + "\n"
        return ret

class Command:
    """
    I am a class that handles a command for a program.
    Commands can be nested underneath a command for further processing.

    @cvar name:        name of the command, lowercase
    @cvar aliases:     list of alternative lowercase names recognized
    @type aliases:     list of str
    @cvar usage:       short one-line usage string;
                       %command gets expanded to a sub-command or [commands]
                       as appropriate
    @cvar summary:     short one-line summary of the command
    @cvar description: longer paragraph explaining the command
    @cvar subCommands: dict of name -> commands below this command
    @type subCommands: dict of str  -> L{Command}
    """
    name = None
    aliases = None
    usage = None
    summary = None
    description = None
    parentCommand = None
    subCommands = None
    subCommandClasses = None
    aliasedSubCommands = None

    def __init__(self, parentCommand=None, stdout=sys.stdout,
        stderr=sys.stderr):
        """
        Create a new command instance, with the given parent.
        Allows for redirecting stdout and stderr if needed.
        This redirection will be passed on to child commands.
        """
        if not self.name:
            self.name = str(self.__class__).split('.')[-1].lower()
        self.stdout = stdout
        self.stderr = stderr
        self.parentCommand = parentCommand

        # create subcommands if we have them
        self.subCommands = {}
        self.aliasedSubCommands = {}
        if self.subCommandClasses:
            for C in self.subCommandClasses:
                c = C(self, stdout=stdout, stderr=stderr)
                self.subCommands[c.name] = c
                if c.aliases:
                    for alias in c.aliases:
                        self.aliasedSubCommands[alias] = c

        # create our formatter and add subcommands if we have them
        formatter = CommandHelpFormatter()
        if self.subCommands:
            for name, command in self.subCommands.items():
                formatter.addCommand(name, command.summary or
                    command.description)

        # expand %command for the bottom usage
        usage = self.usage or self.name
        if usage.find("%command") > -1:
            usage = usage.split("%command")[0] + '[command]'
        usages = [usage, ]

        # walk the tree up for our usage
        c = self.parentCommand
        while c:
            usage = c.usage or c.name
            if usage.find(" %command") > -1:
                usage = usage.split(" %command")[0]
            usages.append(usage)
            c = c.parentCommand
        usages.reverse()
        usage = " ".join(usages)

        # create our parser
        description = self.description or self.summary
        self.parser = optparse.OptionParser(
            usage=usage, description=description,
            formatter=formatter)
        self.parser.disable_interspersed_args()

        # allow subclasses to add options
        self.addOptions()

    def addOptions(self):
        """
        Override me to add options to the parser.
        """
        pass

    def do(self, args):
        """
        Override me to implement the functionality of the command.
        """
        pass

    def parse(self, argv):
        """
        Parse the given arguments and act on them.
        """
        options, args = self.parser.parse_args(argv)

        if hasattr(options, 'help_commands') and options.help_commands:
            # FIXME: we may want to specify program name somehow, instead
            # of the name of the root command
            
            # iterate over all names of parents to construct how we got here
            names = []
            p = self
            while p.parentCommand:
                names.append(p.name)
                p = p.parentCommand
            names.append(p.name)
            names.reverse()
            self.stdout.write("\nType '%s <subcommand> --help' " \
                "for help on a specific subcommand.\n\n" % " ".join(names))

            self.stdout.write("Available subcommands:\n\n")
            keys = self.subCommands.keys()
            keys.sort()
            length = 0
            for key in keys:
                if len(key) > length:
                    length = len(key)
            for name in keys:
                c = self.subCommands[name]
                # FIXME: make output nicer
                format = "%-" + "%d" % length + "s - %s\n"
                self.stdout.write(format % (c.name, c.description))
            self.stdout.write("\n")
            return 0

        ret = self.handleOptions(options)
        if ret:
            return ret

        # if we don't have subcommands, defer to our do() method
        if not self.subCommands:
            return self.do(args)

        # if we do have subcommands, defer to them
        try:
            command = args[0]
        except IndexError:
            self.stderr.write("No command specified.\n")
            self.stderr.write(
                "Use --help to get a list of commands.\n")
            return 1

        if command in self.subCommands.keys():
            return self.subCommands[command].parse(args[1:])

        if self.aliasedSubCommands:
            if command in self.aliasedSubCommands.keys():
                return self.aliasedSubCommands[command].parse(args[1:])

        self.stderr.write("Unknown command '%s'.\n" % command)
        return 1

    def handleOptions(self, options):
        """
        Handle the parsed options.
        """
        pass

    def getRootCommand(self):
        """
        Return the top-level command, which is typically the program.
        """
        c = self
        while c.parentCommand:
            c = c.parentCommand
        return c
