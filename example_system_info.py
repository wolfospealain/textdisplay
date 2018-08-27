#!/usr/bin/python3

from textdisplay import *
import subprocess


class Command:

    def __init__(self, command, options):
        self.command = command
        self.options = options


class Slideshow:
    uptime = Command("uptime",
                     {"delay": 1000, "align": "r", "wrap": True, "text_colour": "lightblue", "font": "TkTextFont"})
    ip = Command(["ip", "addr"],
                 {"delay": 10000, "align": "l", "wrap": False, "text_colour": "lightgreen", "font": "Courier New"})
    ping = Command(["ping", "-c8", "8.8.8.8"],
                   {"delay": 10000, "align": "l", "wrap": False, "text_colour": "orange", "font": "Courier New"})
    df = Command(["df", "-h"],
                 {"delay": 10000, "align": "l", "wrap": False, "text_colour": "yellow", "font": "Courier New"})
    fortune = Command(["fortune", "-s"],
                      {"delay": 20000, "align": "l", "wrap": True, "text_colour": "cyan", "font": "TkTextFont"})
    syslog = Command(["tail", "/var/log/syslog"],
                     {"delay": 10000, "align": "l", "wrap": False, "text_colour": "darkred", "font": "Courier New"})
    users = Command("who",
                    {"delay": 10000, "align": "l", "wrap": False, "text_colour": "white", "font": "Courier New"})
    date = Command("date",
                   {"delay": 1000, "align": "c", "wrap": True, "text_colour": "cyan", "font": "TkTextFont"})
    commands = [fortune] + [uptime] * 20 + [syslog, ip, ping, df, users] + [date] * 20

    def __init__(self):
        self.index = 0

    def run(self):
        output = subprocess.check_output(self.commands[self.index].command, stderr=subprocess.DEVNULL).decode("utf-8")
        options = self.commands[self.index].options
        self.index += 1
        if self.index == len(self.commands):
            self.index = 0
        return (output, options)


app = Slideshow()
display = TextDisplay(app.run, title=sys.argv[0], icon="/usr/share/icons/gnome/256x256/apps/utilities-terminal.png")
