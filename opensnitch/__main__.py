#!/usr/bin/env python3
# This file is part of OpenSnitch.
#
# Copyright(c) 2017 Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
from argparse import ArgumentParser
from os.path import expanduser
import warnings
import logging
import os

from opensnitch.version import VERSION
from opensnitch.snitch import Snitch


if 'SUDO_USER' in os.environ:
    home = expanduser("~%s" % os.environ['SUDO_USER'])
else:
    home = expanduser("~%s" % os.environ['USER'])
filename = os.path.join(home, "opensnitch.db")

parser = ArgumentParser()
parser.add_argument("--log-file", dest="logfile", default=None,
                    help="Log to file.", metavar="FILE")
parser.add_argument("--debug", dest="debug",
                    action="store_true", default=False,
                    help="Enable debug logs.")
parser.add_argument("--database",  dest="database", default=filename,
                    help="Database path.", metavar="FILE")

args = parser.parse_args()


# Ensure Qt4 wont be loaded by matplotlib
try:
    import matplotlib as mpl
except ImportError:
    pass
else:
    mpl.rcParams['backend'] = 'Qt5Agg'


logging.basicConfig(
    format='[%(asctime)s] (%(levelname)s) %(message)s',
    level=logging.INFO if args.debug is False else logging.DEBUG,
    filename=args.logfile)


# At some point Scapy devs will realize how bothering their fucking warnings
# are while importing scapy.all ...
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

warnings.filterwarnings("ignore", category=RuntimeWarning, module="gtk")


if __name__ == '__main__':
    snitch = Snitch(args.database)

    try:
        logging.info("OpenSnitch v%s running with pid %d.",
                     VERSION, os.getpid())
        snitch.start()
    except KeyboardInterrupt as e:
        pass
    finally:
        logging.info("Quitting ...")
        snitch.stop()
