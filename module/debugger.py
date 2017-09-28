
import code
import sys


class Dummy(Exception):
   """Dummy exception raised by debugger to generate an error."""


def debugger(banner='Debugger started (CTRL-D to quit)'):
   """Stops execution and starts console for debugging."""
   # use exception trick to pick up the current frame
   try:
       raise Dummy()
   except Dummy:
       frame = sys.exc_info()[2].tb_frame.f_back

   # evaluate commands in current namespace
   namespace = frame.f_globals.copy()
   namespace.update(frame.f_locals)

   code.interact(banner=banner, local=namespace)
