dnl initialize autoconf
AC_INIT(yq, 0.0.2,
   http://dangerouslyinc.com,
   yq)

dnl initialize automake
AM_INIT_AUTOMAKE

dnl authors
AC_SUBST_FILE(AUTHORS)
AUTHORS=$srcdir/AUTHORS

dnl AM_MAINTAINER_MODE only provides the option to configure to enable it
AM_MAINTAINER_MODE

dnl check for python
AM_PATH_PYTHON(2.4)

dnl check for where to install our python stuff
dnl PYTHONLIBDIR=`$PYTHON -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
PYVER=[`$PYTHON -c "import sys ; print sys.version[:3]"`]
PYTHONLIBDIR=\${libdir}/python$PYVER/site-packages
AC_MSG_NOTICE(Installing python code in $PYTHONLIBDIR)
AC_SUBST(PYTHONLIBDIR)

dnl output stuff
AC_OUTPUT(
Makefile
bin/Makefile
yq/Makefile
yq/command/Makefile
yq/util/Makefile
)
