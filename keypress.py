"""Non-blocking single-keypress reading, on both POSIX and Windows.

POSIX puts the terminal in cbreak mode for the duration and polls with select.
Windows has no select() for console handles, so it uses msvcrt instead.
When stdin is not a terminal (a pipe, a redirect) key() simply never reports
anything, so callers keep running uninterrupted.
"""

import os
import sys

try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import select
    import termios
    import tty
except ImportError:
    termios = None


class KeyReader:
    """Context manager yielding pending keypresses via key()."""

    def __init__(self, stream=None):
        self.stream = sys.stdin if stream is None else stream
        try:
            self.fd = self.stream.fileno()
            self.enabled = os.isatty(self.fd)
        except (AttributeError, ValueError, OSError):
            self.fd = None
            self.enabled = False
        self.oldSettings = None

    def __enter__(self):
        if self.enabled and msvcrt is None and termios is not None:
            self.oldSettings = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        return self

    def __exit__(self, *exc):
        if self.oldSettings is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.oldSettings)
            self.oldSettings = None
        return False

    def key(self):
        """Return the pending keypress lowercased, or None if there is none."""
        if not self.enabled:
            return None

        if msvcrt is not None:
            if not msvcrt.kbhit():
                return None
            char = msvcrt.getwch()
            # Arrows and function keys arrive as a prefix plus a scan code;
            # swallow the second half so it is not read as a separate key.
            if char in ('\x00', '\xe0'):
                msvcrt.getwch()
                return None
            return char.lower()

        if select.select([self.stream], [], [], 0)[0]:
            return self.stream.read(1).lower()
        return None
