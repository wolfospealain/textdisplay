#!/usr/bin/python3

from textdisplay import *
import subprocess


class Command:

    def __init__(self, command, options):
        self.command = command
        self.options = options


class Slideshow:
    cyan = Command(["fortune", "-s"],
                   {"delay": 30000, "align": "l", "wrap": True, "text_colour": "cyan", "font": "TkTextFont"})
    yellow = Command(["fortune", "-s"],
                     {"delay": 30000, "align": "l", "wrap": True, "text_colour": "yellow", "font": "TkTextFont"})
    green = Command(["fortune", "-l"],
                    {"delay": 50000, "align": "l", "wrap": False, "text_colour": "lightgreen", "font": "TkTextFont"})
    orange = Command(["fortune", "-s"],
                     {"delay": 30000, "align": "l", "wrap": True, "text_colour": "orange", "font": "TkTextFont"})
    blue = Command(["fortune", "-s"],
                   {"delay": 30000, "align": "l", "wrap": True, "text_colour": "lightblue", "font": "TkTextFont"})
    commands = [cyan, yellow, green, orange, blue]

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
