#!/usr/bin/python3

"""
Python module (and standalone command-line tool) to easily pipe information to a large text fullscreen/windowed GUI.
https://github.com/wolfospealain/textdisplay
Wolf Ó Spealain, 2018
"""

from tkinter import *
from tkinter import font


class TextDisplay:
    """Creates a GUI screen to display the updated output of the text_source function, and repeat after delay."""

    def __init__(self, command, delay=1000, title="", icon="", align="l", colour="lightgreen",
                 background="black", font="Courier", typing_mode=False, wrap=False, size=0):
        self.update = command
        self.delay = delay
        self.screen = Tk(className=title)
        self.screen.wm_iconphoto(True, PhotoImage(file=icon))
        self.screen.title(title)
        self.align = align[0]
        self.colour = colour
        self.background = background
        self.font = font
        self.typing_mode = typing_mode
        self.wrap = wrap if not self.typing_mode else True
        self.screen.configure(background=self.background)
        self.screen.resizable(width=YES, height=YES)
        self.screen.attributes("-fullscreen", True)
        self.screen.bind("<F11>", self.toggle_fullscreen)
        self.screen.bind("<Escape>", self.quit)
        self.text = ""
        if size != 0 and not self.typing_mode:
            self.size = size
            self.auto_font_size = False
        else:
            self.size = 12
            self.auto_font_size = True
        self.textbox = Text(self.screen, font=(self.font, size, 'bold'), bg=background,
                            fg=self.colour if self.typing_mode else self.background, border=0, relief=FLAT,
                            highlightbackground=self.background, wrap=WORD if self.wrap else NONE)
        self.textbox.pack(expand=True, fill=BOTH, padx=50, pady=50)
        if self.typing_mode:
            self.textbox.configure(insertbackground=self.colour)
            self.textbox.bind("<F5>", self.textbox_refresh)
            self.textbox.bind("<Key>", self.textbox_focus)
            self.textbox.bind("<1>", self.textbox_focus)
            self.textbox.delete("1.0", END)
            self.textbox.insert(INSERT, self.text, "text")
            self.textbox.tag_config("text", justify=self.align)
            self.textbox.focus_set()
        else:
            self.screen.after(self.delay, self.tick, self.delay)
        self.screen.mainloop()

    def quit(self, event):
        exit()

    def textbox_focus(self, event):
        self.textbox.configure(insertbackground=self.colour)

    def textbox_refresh(self, event):
        self.tick(False)

    def toggle_fullscreen(self, event=None):
        self.screen.attributes("-fullscreen", not self.screen.attributes("-fullscreen"))

    def end_fullscreen(self, event=None):
        self.screen.attributes("-fullscreen", False)

    def visibility(self, textbox, wrappable=True):
        """Return the visibility of in a tkinter Text widget: false if cropped."""
        character_font = font.Font(family=self.font, size=self.size, weight='bold')
        text = textbox.get("1.0", END).split("\n")[:-1]
        if not wrappable:
            widest_line = 0
            for line in range(0, len(text)):
                if len(text[line]) > len(text[widest_line]):
                    widest_line = line
            visible = character_font.measure(text[widest_line]) <= textbox.winfo_width()
        else:
            bounding_box = textbox.bbox("end-1c")
            visible = bounding_box and bounding_box[3] >= character_font.metrics('linespace')
        return visible

    def tick(self, delay=False):
        if not self.typing_mode:
            text, options = self.update()
            text = text.strip()
            if options:
                if "delay" in options:
                    delay = options["delay"]
                if "wrap" in options:
                    self.wrap = options["wrap"]
                    self.textbox.config(wrap=WORD if self.wrap else NONE)
                if "align" in options:
                    self.align = options["align"]
                if "text_colour" in options:
                    self.colour = options["text_colour"]
                if "font" in options:
                    self.font = options["font"]
                    self.textbox.config(font=(self.font, self.size, "bold"))
            if text:
                self.text = text
            self.textbox.delete("1.0", END)
            self.textbox.insert(INSERT, self.text, "text")
            self.textbox.tag_config("text", justify=self.align)
        else:
            self.textbox.config(insertbackground=self.background)
        if self.wrap:
            self.textbox.see("1.0")
        if self.auto_font_size:
            # find maximum font size
            if self.visibility(self.textbox, self.wrap):
                while self.visibility(self.textbox, self.wrap):
                    self.size += 1
                    self.textbox.config(font=(self.font, self.size, "bold"))
                self.size -= 1
                self.textbox.config(font=(self.font, self.size, "bold"))
            else:
                while not self.visibility(self.textbox, self.wrap) and self.size > 1:
                    self.size -= 1
                    self.textbox.config(font=(self.font, self.size, "bold"))
        # vertically centre text
        if self.visibility(self.textbox, wrappable=True) == 1:
            space = self.textbox.winfo_height() - (self.textbox.bbox("end-1c")[1] + self.textbox.bbox("end-1c")[3])
            line_height = font.Font(family=self.font, size=self.size, weight='bold').metrics('linespace')
            lines = int(space / line_height / 2)
            self.textbox.insert("1.0", "\n" * lines)
        self.textbox.config(fg=self.colour)
        self.screen.update_idletasks()
        if delay:
            self.screen.after(delay, self.tick, delay)


if __name__ == "__main__":
    import sys
    import os
    import subprocess
    import argparse


    def install(target, name):
        """Install to target path and set executable permission."""
        if os.path.isdir(target):
            try:
                subprocess.check_output(["cp", sys.argv[0], target + "/" + name]).decode("utf-8")
                subprocess.check_output(["chmod", "a+x", target + "/" + name]).decode("utf-8")
                print("Installed to " + target + " as " + name + ".\n")
            except:
                print("Not installed.")
                if os.getuid() != 0:
                    print("Is sudo required?\n")
                return False
        else:
            print(target, "is not a directory.\n")
            return False


    def parse_command_line():
        parser = argparse.ArgumentParser(
            description="%(prog)s " + "Python module (and standalone command-line tool) to easily pipe information to a large text fullscreen/windowed GUI. https://github.com/wolfospealain/textdisplay",
            epilog="ESC to exit, or F11 to toggle fullscreen.")
        if ".py" in sys.argv[0]:
            parser.add_argument("--install", action="store_true", dest="install", default=False,
                                help="install to Linux /usr/local/bin")
        parser.add_argument("-a", "--align", action="store", dest="align", default="left",
                            help="align text horizontally: l/left, r/right, c/centre")
        parser.add_argument("-b", "--background", action="store", dest="background", default="black",
                            help="background colour")
        parser.add_argument("-c", "--colour", action="store", dest="colour", default="lightgreen",
                            help="text colour (see https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm)")
        parser.add_argument("-d", "--delay", action="store", dest="delay", default=1000,
                            help="update delay in ms (default: 1000)")
        parser.add_argument("-f", "--font", action="store", dest="font", default="TkFixedFont",
                            help="font (see https://tkdocs.com/tutorial/fonts.html)")
        parser.add_argument("-l", "--lines", action="store", dest="lines", type=int, default=0,
                            help="number of lines to display (default: all)")
        parser.add_argument("-s", "--font-size", action="store", dest="size", type=int, default=0,
                            help="font size (default: auto)")
        parser.add_argument("-t", "--typing-mode", action="store_true", dest="typing", default=False,
                            help="direct entry mode (F5 to automatically resize text)")
        parser.add_argument("-w", "--wrap", action="store_true", dest="wrap", default=False,
                            help="line wrap, single page")
        args = parser.parse_args()
        return args


    def text_source():
        """Test text_source function: reads from stdin."""
        if args.lines == 1:
            text = sys.stdin.readline().strip()
        elif args.lines == 0:
            text = sys.stdin.read()
        else:
            text = ""
            for line in range(0, args.lines - 1):
                text += sys.stdin.readline()
            text += sys.stdin.readline().strip()
        return (text, None)


    args = parse_command_line()
    if ".py" in sys.argv[0]:
        if args.install:
            install("/usr/local/bin", "textdisplay")
            exit()
    display = TextDisplay(text_source, title=sys.argv[0], align=args.align, colour=args.colour,
                          background=args.background,
                          font=args.font, size=args.size, delay=args.delay, typing_mode=args.typing,
                          wrap=args.wrap, icon="/usr/share/icons/gnome/256x256/apps/utilities-terminal.png")
