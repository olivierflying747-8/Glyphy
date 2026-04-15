# asciify.py & deasciify.py help you edit a bitmap array in a visual way.

Usage:<br>
<br>
- Open `asciify.py`
- Paste your ProffieOS bitmap array into `GLYPH`
- Save
- Open a console
- Run: `python asciify.py`
- `asciified.txt` will open in your text editor
- Modify your glyph using only `" "` & `"█"` (add "0b" & "UL" as necessary if you increase the width)
- Save
- Run: `python deasciify.py`
- `deasciified.txt` will open in your text editor
- Copy your bitmap array and paste it back in your ProffieOS text font
- Save your font
<br>
Note:<br>
- The input bitmap must be rectangular
<br>
<br>
<br>
# fontconvert.py is identical to ProffieOS/fontconvert/fontconvert.c
fontconvert.py will convert a TTF to a .h ProffieOS font

Usage:<br>
- Run: python fontconvert.py YourFont.ttf 10 > YourFont.h
<br>
<br>
<br>
# rotate_flips.py allows to rotate and/or flip a ProffieOS bitmap

Usage:<br>
<br>
- Open `rotate_flips.py`
- Paste your ProffieOS bitmap array into `GLYPH`
- Save
- Open a console
- Run: `python rotate_flips.py`
- `rotated_flipped.txt` will open in your text editor
