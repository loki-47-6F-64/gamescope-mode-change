#!/usr/bin/python

import sys
import os

# Change path so we find Xlib
sys.path.append(os.path.join(os.path.dirname(__file__), 'third-party/python-xlib'))

atomName = "GAMESCOPE_XWAYLAND_MODE_CONTROL"

from optparse import OptionParser
from Xlib import display, Xatom, X

from Xlib.protocol import event
from Xlib.xobject import drawable

parser = OptionParser()
parser.add_option("-d", "--display", dest="display", help="This option specifies the X server to which to connect", metavar="dpy", default=":1")
parser.add_option("-x", "--nestedWidth", dest="width", help="The width as seen by the Game, if width is 0, then Gamescope's output resolution will be used", metavar="nested_width", default="1280")
parser.add_option("-y", "--nestedHeight", dest="height", help="The height as seen by the Game, if height is 0, then Gamescope's output resolution will be used", metavar="nested_height", default="800")
parser.add_option("-i", "--id", dest="serverID", help="The xwayland server to modify: [0 .. n) where n is the number of xwayland servers setup by Gamescope, e.g. --id=0 will modify the first xwayland server", metavar="serverID", default="0")
parser.add_option("-f", "--force", action="store_true", dest="force", help="Force resolution even if the width and/or the height exceed the Gamescope output width/height respectively", default=False)

(options, args) = parser.parse_args()

width = int(options.width)
height = int(options.height)
serverID = int(options.serverID)

MAX_INT = 2**30 + (2**30-1)
superRes = 1 if options.force else 0

if(height == 0 or width == 0):
  height = MAX_INT
  width = MAX_INT
  superRes = 0

d = display.Display(options.display)

atom = d.intern_atom(atomName, only_if_exists=1)
if atom == X.NONE:
  sys.stderr.write('xwayland:  no atom named "%s" on server "%s"\n'%(atomName, d.get_display_name()))
  sys.exit(1)

print(d.screen().root.id)


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

def _changeMode(disp : display.Display, atom : int, win : drawable.Window, width : int, height : int, serverID = 1, superRes = 1):
  print(f"changeMode({win.id})")
  win.change_property(atom, Xatom.CARDINAL, 32, [serverID, width, height, superRes])

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

changeMode(d.screen().root, width, height, serverID, superRes)
sendModeChanged(d.screen().root)