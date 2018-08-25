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

    def __init__(self, text_source, delay=1000, title="", icon="", text_colour="lightgreen", background_colour="black",
                 font_face="Courier", typing_mode=False, multi_line_wrap=False, font_size=0):
        self.update = text_source
        self.delay = delay
        self.screen = Tk(className=title)
        self.screen.wm_iconphoto(True, PhotoImage(file=icon))
        self.screen.title(title)
        self.text_colour = text_colour
        self.background_colour = background_colour
        self.font_face = font_face
        self.typing_mode = typing_mode
        self.multi_line_wrap = multi_line_wrap if not self.typing_mode else True
        self.screen.configure(background=self.background_colour)
        self.screen.resizable(width=YES, height=YES)
        self.screen.attributes("-fullscreen", True)
        self.screen.bind("<F11>", self.toggle_fullscreen)
        self.screen.bind("<Escape>", self.end_fullscreen)
        self.text = ""
        if font_size != 0 and not self.typing_mode:
            self.font_size = font_size
            self.auto_font_size = False
        else:
            self.font_size = 12
            self.auto_font_size = True
        self.textbox = Text(self.screen, font=(self.font_face, font_size, 'bold'), bg=self.background_colour,
                            fg=self.text_colour if self.typing_mode else self.background_colour, border=0, relief=FLAT,
                            highlightbackground=self.background_colour, wrap=WORD if self.multi_line_wrap else NONE)
        self.textbox.pack(expand=True, fill="both", padx=50, pady=50)
        if self.typing_mode:
            self.textbox.configure(insertbackground=self.text_colour)
            self.textbox.bind("<F5>", self.textbox_refresh)
            self.textbox.bind("<Key>", self.textbox_focus)
            self.textbox.bind("<1>", self.textbox_focus)
            self.textbox.delete("1.0", END)
            self.textbox.insert(INSERT, self.text)
        else:
            self.screen.after(self.delay, self.tick, self.delay)
        self.screen.mainloop()

    def textbox_focus(self, event):
        self.textbox.configure(insertbackground=self.text_colour)

    def textbox_refresh(self, event):
        self.tick(False)

    def toggle_fullscreen(self, event=None):
        self.screen.attributes("-fullscreen", not self.screen.attributes("-fullscreen"))

    def end_fullscreen(self, event=None):
        self.screen.attributes("-fullscreen", False)

    def visibility(self, textbox, wrappable=True):
        """Return the visibility of rows and columns in a tkinter Text widget: false if cropped."""
        character_font = font.Font(family=self.font_face, size=self.font_size, weight='bold')
        line_height = character_font.metrics('linespace')
        text = textbox.get("1.0", END).split("\n")[:-1]
        lines = len(text)
        visible_rows = False
        visible_columns = False
        # scrollable, with no line wrapping
        if not wrappable:
            widest_line = 0
            for line in range(0, lines):
                if len(text[line]) > len(text[widest_line]):
                    widest_line = line
            if character_font.measure(text[widest_line]) <= textbox.winfo_width():
                visible_columns = True
        else:
            # check first character visibility for every line (including line height)
            for line in range(1, lines + 1):
                bounding_box = textbox.bbox("%d.%d" % (line, 0))
                if bounding_box and bounding_box[3] >= line_height:
                    visible_rows = True
                    # check last character visibility (including line height and font width)
                    character = len(text[line - 1]) - 1
                    if character > -1:
                        bounding_box = textbox.bbox("%d.%d" % (line, character))
                        if bounding_box and bounding_box[2] >= character_font.measure(text[line - 1][character]) and \
                                bounding_box[3] >= line_height:
                            visible_columns = True
                        else:
                            visible_columns = False
                elif visible_rows:
                    visible_rows = False
                    break
                if visible_rows and not visible_columns:
                    break
        return visible_rows, visible_columns

    def tick(self, delay=False):
        if not self.typing_mode:
            text = self.update().strip()
            if text:
                self.text = text
                self.textbox.delete("1.0", END)
                self.textbox.insert(INSERT, self.text)
        else:
            self.textbox.configure(insertbackground=self.background_colour)
        if self.multi_line_wrap:
            self.textbox.see("1.0")
        if self.auto_font_size:
            row, col = self.visibility(self.textbox, self.multi_line_wrap)
            if (not self.multi_line_wrap or row) and col:
                while (not self.multi_line_wrap or row) and col:
                    self.font_size += 1
                    self.textbox.config(font=(self.font_face, self.font_size, "bold"))
                    row, col = self.visibility(self.textbox, self.multi_line_wrap)
                self.font_size -= 1
                self.textbox.config(font=(self.font_face, self.font_size, "bold"))
            else:
                while ((self.multi_line_wrap and not row) or not col) and self.font_size > 1:
                    self.font_size -= 1
                    self.textbox.config(font=(self.font_face, self.font_size, "bold"))
                    row, col = self.visibility(self.textbox, self.multi_line_wrap)
        self.textbox.config(fg=self.text_colour)
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


    def parse_command_line(description):
        parser = argparse.ArgumentParser(description="%(prog)s " + description)
        if ".py" in sys.argv[0]:
            parser.add_argument("--install", action="store_true", dest="install", default=False,
                                help="install to Linux destination path (default: " + install_path + ")")
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
        parser.add_argument("-p", "--page", action="store_true", dest="page", default=False,
                            help="fill page, multi-line wrap")
        parser.add_argument("-s", "--font-size", action="store", dest="size", type=int, default=0,
                            help="font size (default: auto)")
        parser.add_argument("-t", "--typing-mode", action="store_true", dest="typing", default=False,
                            help="direct entry mode (F5 to automatically resize text)")
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
        return text


    install_path = "/usr/local/bin"
    name = "textdisplay"
    description = "Python module (and standalone command-line tool) to easily pipe information to a large text fullscreen/windowed GUI. https://github.com/wolfospealain/textdisplay"

    args = parse_command_line(description)
    if ".py" in sys.argv[0]:
        if args.install:
            install(install_path, name)
            exit()
    display = TextDisplay(text_source, title=sys.argv[0], text_colour=args.colour, background_colour=args.background,
                          font_face=args.font, font_size=args.size, delay=args.delay, typing_mode=args.typing,
                          multi_line_wrap=args.page, icon="/usr/share/icons/gnome/256x256/apps/utilities-terminal.png")
