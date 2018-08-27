#!/usr/bin/python3

from textdisplay import *
from decimal import *

def pi():
    """Compute Pi to the current precision.

    >>> print(pi())
    3.141592653589793238462643383

    https://docs.python.org/3/library/decimal.html#recipes
    """
    getcontext().prec += 2  # extra digits for intermediate steps
    three = Decimal(3)      # substitute "three=3.0" for regular floats
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n+na, na+8
        d, da = d+da, da+32
        t = (t * n) / d
        s += t
    getcontext().prec -= 2
    return +s               # unary plus applies the new precision

class Application:

    def __init__(self):
        self.precision = 1
        self.pi = Decimal(0)

    def run(self):
        getcontext().prec = self.precision
        self.pi = pi()
        self.precision += 1
        return (str(self.pi), None)

app = Application()
display = TextDisplay(app.run, delay=10, title=sys.argv[0], wrap=True, align="r", font="TkTextFont",
                      colour="cyan", icon="/usr/share/icons/gnome/256x256/apps/utilities-terminal.png")
