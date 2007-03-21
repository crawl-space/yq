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

        try:
            os.mkdir("/var/lib/yq")
        except OSError, e:
            if e.errno == 17:
                # the directory already exists. we can ignore this
                pass
            else:
                raise

        if os.path.exists("/var/lib/yq/series") or \
                os.path.exists("/var/lib/yq/status") or \
                os.path.exists("/var/lib/yq/base"):
            print "yq data already exists"
            return 255

        series = open("/var/lib/yq/series", 'w')
        series.close()

        series = open("/var/lib/yq/status", 'w')
        series.close()

        base = open("/var/lib/yq/base", 'w')

        ts = rpm.TransactionSet()
        mi = ts.dbMatch()

        for pkg in mi:
            print >> base, "%s %s %s %s %s" % (pkg['name'], pkg['epoch'], pkg['version'], pkg['release'], pkg['arch'])

        base.close()
