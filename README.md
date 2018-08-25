# textdisplay
Python module (and standalone command-line tool) to easily pipe information to a large text fullscreen/windowed GUI.
```
usage: textdisplay.py [-h] [--install] [-b BACKGROUND] [-c COLOUR] [-d DELAY]
                      [-f FONT] [-l LINES] [-p] [-s SIZE] [-t]

textdisplay.py Python module (and standalone command-line tool) to easily pipe
information to a large text fullscreen/windowed GUI.
https://github.com/wolfospealain/textdisplay

optional arguments:
  -h, --help            show this help message and exit
  --install             install to Linux destination path (default:
                        /usr/local/bin)
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
  -p, --page            fill page, multi-line wrap
  -s SIZE, --font-size SIZE
                        font size (default: auto)
  -t, --typing-mode     direct entry mode (F5 to automatically resize text)
```
