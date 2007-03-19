# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command

class Pop(command.Command):
    summary = "pop a transaction off the stack"
    description = """This command will pop the most recently applied transaction off the stack. All changes to your system will be reversed."""

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import os
        from yum import YumBase

        my_yum = YumBase()
        series = open("/var/lib/yq/status", 'r')
        for line in series: pass
        transaction_name = line.strip()
        transaction = open(os.path.join("/var/lib/yq/", transaction_name), 'r')

        for line in transaction:
            line = line.strip()
            parts = line.split(' ')
            if parts[0] == '-':
                fn = my_yum.install
            elif parts[0] == '+':
                fn = my_yum.remove
            else:
                assert False, "corrupt transaction file"

            if parts[2] == 'None':
                parts[2] = 0
            fn(name=parts[1], epoch=parts[2], version=parts[3],
                    release=parts[4], arch=parts[5])

        dlpkgs = map(lambda x: x.po, filter(lambda txmbr:
                                            txmbr.ts_state in ("i", "u"),
                                            my_yum.tsInfo.getMembers()))
        my_yum.downloadPkgs(dlpkgs)

        my_yum.initActionTs() # make a new, blank ts to populate
        my_yum.populateTs(keepold=0)
        my_yum.ts.check() #required for ordering
        my_yum.ts.order() # order

        # FIXME: is it really sane to use this from here?
        import sys
        sys.path.append('/usr/share/yum-cli')
        import callback

        cb = callback.RPMInstallCallback(output = 0)
        cb.filelog = True
        cb.tsInfo = my_yum.tsInfo
        my_yum.runTransaction(cb)

        #Remove from the series
        #yes, this will eat files and babies
        series = open("/var/lib/yq/status", 'r')
        lines = series.readlines()
        series.close()
        series = open("/var/lib/yq/status", 'w')
        for line in lines[:-1]:
            series.write(line)
        series.close()
