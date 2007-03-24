# vi:si:et:sw=4:sts=4:ts=4

from yq.util import config


def list_installed():
    import rpm

    ts = rpm.TransactionSet()
    mi = ts.dbMatch()

    current_pkgs = []
    for pkg in mi:
        current_pkgs.append("%s %s %s %s %s\n" % (pkg['name'], pkg['epoch'],
            pkg['version'], pkg['release'], pkg['arch']))
    return current_pkgs

def push(transaction_name):
    _run_transaction(transaction_name, '+', '-')

def pop(transaction_name):
    _run_transaction(transaction_name, '-', '+')

def _run_transaction(transaction_name, install_mode, remove_mode):
    import os
    from yum import YumBase

    transaction = open(os.path.join(config.STACKDIR, transaction_name),
            'r')

    my_yum = YumBase()
    
    for line in transaction:
        line = line.strip()
        parts = line.split(' ')
        if parts[0] == install_mode:
            fn = my_yum.install
        elif parts[0] == remove_mode:
            fn = my_yum.remove
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
