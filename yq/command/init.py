# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Init(command.Command):
    summary = "initialize the yq data"
    description = """This command will create the files and directories needed by yq."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import os
        import rpm

        os.mkdir("/var/lib/yq")
        series = open("/var/lib/yq/series", 'w')
        series.close()

        base = open("/var/lib/yq/base", 'w')

        ts = rpm.TransactionSet()
        mi = ts.dbMatch()

        for pkg in mi:
            print >> base, "%s %s %s %s %s" % (pkg['name'], pkg['epoch'], pkg['version'], pkg['release'], pkg['arch'])

        base.close()
