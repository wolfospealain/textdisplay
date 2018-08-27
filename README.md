# textdisplay
Python module (and standalone command-line tool) to easily pipe information to a large text fullscreen/windowed GUI.
```
usage: textdisplay.py [-h] [--install] [-a ALIGN] [-b BACKGROUND] [-c COLOUR]
                      [-d DELAY] [-f FONT] [-l LINES] [-s SIZE] [-t] [-w]

textdisplay.py Python module (and standalone command-line tool) to easily pipe
information to a large text fullscreen/windowed GUI.
https://github.com/wolfospealain/textdisplay

optional arguments:
  -h, --help            show this help message and exit
  --install             install to Linux /usr/local/bin
  -a ALIGN, --align ALIGN
                        align text horizontally: l/left, r/right, c/centre
  -b BACKGROUND, --background BACKGROUND
                        background colour
  -c COLOUR, --colour COLOUR
                        text colour (see
                        https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm)
  -d DELAY, --delay DELAY
                        update delay in ms (default: 1000)
  -f FONT, --font FONT  font (see https://tkdocs.com/tutorial/fonts.html)
  -l LINES, --lines LINES
                        number of lines to display (default: all)
  -s SIZE, --font-size SIZE
                        font size (default: auto)
  -t, --typing-mode     direct entry mode (F5 to automatically resize text)
  -w, --wrap            line wrap, single page

ESC to exit, or F11 to toggle fullscreen.

```
## Use Cases
Signage.

Impromptu/backup signage.

Multiple monitors

Live feed displays (e.g. train arrivals/departures).

System monitoring.

"Out of Order" computer notice.

Personal computer/office notices.

Countdowns, timers.

Teacher presentations.

GUI output for Python text programs.

Add a desktop shortcut key for "/usr/local/bin/textdisplay -t" for instant notices.

### Linux Command-Line Examples
Calendar ```ncal -h | ./textdisplay.py -p -f courier```

Ping ```ping 8.8.8.8 | ./textdisplay.py  -l 1 -p -c cyan```

Fortune ```while true; do fortune -s; sleep 60; done | ./textdisplay.py -l 1 -p -c yellow```

Uptime ```while true; do uptime; sleep 1; done | ./textdisplay.py -l 1 -p -c orange -d 30000```
