# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Init(command.Command):
    summary = "initialize the yq data"
    description = """This command will create the files and directories needed by yq."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import os
        from yq.backend import yumbackend

        try:
            os.mkdir(config.STACKDIR)
        except OSError, e:
            if e.errno == 17:
                # the directory already exists. we can ignore this
                pass
            else:
                raise

        if os.path.exists(config.SERIES) or \
                os.path.exists(config.STATUS) or \
                os.path.exists(config.BASE):
            print "yq data already exists"
            return 255

        series = open(config.SERIES, 'w')
        series.close()

        status = open(config.STATUS, 'w')
        status.close()

        installed = yumbackend.list_installed()
        base = open(config.BASE, 'w')
        base.writelines(installed)
        base.close()
