#!/usr/bin/python

import sys
import os

# Change path so we find Xlib
sys.path.append(os.path.join(os.path.dirname(__file__), 'third-party/python-xlib'))

from optparse import OptionParser
from Xlib import display, Xatom, X

from Xlib.protocol import event
from Xlib.xobject import drawable

parser = OptionParser()
parser.add_option("-d", "--display", dest="display", help="This option specifies the X server to which to connect", metavar="dpy", default=":1")
parser.add_option("-r", "--refresh-rate", dest="refreshRate", help="The refresh rate in FPS", metavar="fps", default="0")
parser.add_option("-x", "--dynamic", action="store_true", dest="dynamic", help="Adjust dynamic refresh rate rather than the FPS limit", default=False)

(options, args) = parser.parse_args()

atomName = "GAMESCOPE_DYNAMIC_REFRESH" if options.dynamic else "GAMESCOPE_FPS_LIMIT"
refreshRate = int(options.refreshRate)

d = display.Display(options.display)

atom = d.intern_atom(atomName, only_if_exists=1)
if atom == X.NONE:
  sys.stderr.write('xwayland:  no atom named "%s" on server "%s"\n'%(atomName, d.get_display_name()))
  sys.exit(1)


def _sendModeChanged(disp : display.Display, atom : int, win : drawable.Window):
  event_ = event.PropertyNotify(
    window = win.id,
    display = disp,
    atom = atom,
    time = 0,
    state = X.PropertyNewValue
  )

  win.send_event(event_)
  disp.flush()

def _changeMode(disp : display.Display, atom : int, win : drawable.Window, fps : int):
  win.change_property(atom, Xatom.CARDINAL, 32, [fps])

def x11(disp : display.Display, func, *args):
  ret = func(disp, *args)

  disp.flush()

  return ret

def apply(f, *args1):
  def _apply(*args2):
    f(*args1, *args2)
  return _apply


sendModeChanged = apply(x11, d, _sendModeChanged, atom)
changeMode = apply(x11, d, _changeMode, atom)

changeMode(d.screen().root, refreshRate)
sendModeChanged(d.screen().root)