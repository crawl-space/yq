# vi:si:et:sw=4:sts=4:ts=4

from yq.util import command
from yq.util import config

class Push(command.Command):
    summary = "push a transaction onto the stack"
    description = """This command will push the next transaction onto the stack, modifing the system.""" 

    def handleOptions(self, options):
        self.options = options

    def do(self, args):
        import os
        from yum import YumBase
        from yq import stack

        my_yum = YumBase()

        transaction_name = stack.next()
        transaction = open(os.path.join(config.STACKDIR, transaction_name),
                'r')

        for line in transaction:
            line = line.strip()
            parts = line.split(' ')
            if parts[0] == '-':
                fn = my_yum.remove
            elif parts[0] == '+':
                fn = my_yum.install
            else:
                assert False, "corrupt transaction file"

            if parts[2] == 'None':
                parts[2] = None
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
        status = open(config.STATUS, 'a')
        print >> status, transaction_name
        status.close()
