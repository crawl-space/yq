# vi:si:et:sw=4:sts=4:ts=4

import sys

from yq.util import command

from yq.command import init
from yq.command import new
from yq.command import refresh
from yq.command import pop
from yq.command import push
from yq.command import top
from yq.command import helpcmd
from yq.command import series
from yq.command import applied


class Yq(command.Command):
    usage = "%prog %command"
    description = """yq is quilt for packages."""

    subCommandClasses = [init.Init, new.New, refresh.Refresh, pop.Pop,
            push.Push, top.Top, helpcmd.Help, series.Series, applied.Applied]

    def addOptions(self):
        self.parser.add_option('', '--version',
                          action="store_true", dest="version",
                          help="show version information")

    def handleOptions(self, options):
        if options.version:
            print "0.0.1"
            sys.exit(0)


def main(argv):
    c = Yq()
    try:
        ret = c.parse(argv)
    except SystemError, e:
        sys.stderr.write('yq: error: %s\n' % e.args)
        return 255

    if ret is None:
        return 0
    return ret
