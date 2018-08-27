#!/usr/bin/python3

from textdisplay import *
import time


def clock():
    return (time.strftime('%H:%M'), None)


display = TextDisplay(clock, delay=1000, title=sys.argv[0], wrap=True, align="c", font="Impact",
                      colour="darkred", icon="/usr/share/icons/gnome/256x256/apps/utilities-terminal.png")
