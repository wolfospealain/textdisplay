#!/usr/bin/python3

from textdisplay import *
from datetime import datetime


def clock():
    brexit = datetime(2019, 3, 29, 23, 0, 0)
    difference = brexit - datetime.now()
    days = difference.days
    minutes, seconds = divmod(difference.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    countdown = "%d days\n%02d hours\n%02d minutes\n%02d seconds" % (days, hours, minutes, seconds)
    return (countdown, None)


display = TextDisplay(clock, delay=100, title=sys.argv[0], wrap=True, align="l", font="TkTextFont",
                      colour="cyan", icon="/usr/share/icons/gnome/256x256/apps/utilities-terminal.png")
