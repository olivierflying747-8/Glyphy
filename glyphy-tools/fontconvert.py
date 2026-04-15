#!/usr/bin/env python3

"""
ProffieOS font converter (Python version)

Based on:
TrueType to Adafruit_GFX font converter. Derived from Peter Jakobs'
Adafruit_ftGFX fork & makefont tool, and Paul Kourany's Adafruit_mfGFX.

NOT AN ARDUINO SKETCH. This is a command-line tool for preprocessing
fonts to be used with the Adafruit_GFX Arduino librar and/or ProffieOS.

Outputs to stdout. Redirect to a header file:
  python fontconvert.py font.ttf 18 > font.h

REQUIRES FREETYPE (freetype-py)
In cmd window, run once: pip install freetype-py

Currently extracts printable 7-bit ASCII characters of a font.
"""
"""
Quick start:
  python fontconvert.py YourFont.ttf 10 > YourFont.h
"""
"""
▶ Running FONTCONVERT
Navigate to the folder containing fontconvert.py (ProffieOS/display/glyphy-tools)
Right click on the "glyphy-tools" folder in left pane window (Windows Explorer)
Click on "Open command window here"
Run:
python fontconvert.py Starjedi.ttf 10 > StarJedi10.h
  or
python fontconvert.py Aurebesh.ttf 10 > Aurebesh10.h
  or
...
"""

import freetype
import os
import sys

from PIL import Image, ImageDraw, ImageFont

RENDER_ENGINE = "freetype"  # "freetype" | "pillow_mono" | "pillow_aa"
# RENDER_ENGINE = "freetype"     # production
# RENDER_ENGINE = "pillow_mono"  # alternative look
# RENDER_ENGINE = "pillow_aa"    # experimental / nicer shapes

PILLOW_EXTRA_SPACING = 1    # added to advance in "pillow" modes

DESCENDERS = False          # set to True if font has descending characters

AA_THRESHOLD = 128          # used only for pillow_aa

DPI = 141                   # Approximate resolution used in original tool

# --------------------------------------------------
# FONT NAME SANITIZATION
# --------------------------------------------------
def sanitize_font_name(path, size, last_char):
  """
  Derive font table name from filename.

  - Strip path
  - Remove extension
  - Append size and bit depth
  - Replace spaces/punctuation with underscores
  """

  name = os.path.basename(path)
  name = os.path.splitext(name)[0]

  # ----- Append size and 7/8 bit flag -----
  name += f"{size}pt{'8' if last_char > 127 else '7'}b"

  # ----- Replace spaces & punctuation with underscores -----
  return "".join(c if c.isalnum() else "_" for c in name)

# --------------------------------------------------
# MAIN CONVERSION FUNCTION
# --------------------------------------------------
def convert_font(font_path, size, first=32, last=126):
  """
  Convert TrueType font into ProffieOS-compatible header.

  Arguments:
    font_path : path to .ttf file
    size      : font size
    first     : first ASCII char (default ' ')
    last      : last ASCII char (default '~')
  """

  # --------------------------------------------------
  # Init FreeType and load font
  # --------------------------------------------------
  face = freetype.Face(font_path)

  # ----- << 6 because '26.6' fixed-point format -----
  face.set_char_size(size * 64, 0, DPI, 0)

  font_name = sanitize_font_name(font_path, size, last)

  bitmap_offset = 0
  glyph_table = []
  bytes_used = 0

  # --------------------------------------------------
  # Process glyphs
  # --------------------------------------------------
  if RENDER_ENGINE in ("pillow_mono", "pillow_aa"):
    font = ImageFont.truetype(font_path, size)

  for i in range(first, last + 1):

    if RENDER_ENGINE == "freetype":
      # Load and render glyph in MONO mode
      # MONO renderer provides clean image with perfect crop
      try:
        face.load_char(chr(i), freetype.FT_LOAD_TARGET_MONO)
        face.glyph.render(freetype.FT_RENDER_MODE_MONO)
      except Exception as e:
        print(f"Error loading char '{chr(i)}': {e}", file=sys.stderr)
        continue

      slot = face.glyph
      bitmap = slot.bitmap

      # ----- Glyph metrics -----
      width = bitmap.width
      height = bitmap.rows

      xAdvance = slot.advance.x >> 6
      xOffset = slot.bitmap_left
      yOffset = 1 - slot.bitmap_top  # IMPORTANT: exact match to C

      def get_pixel(x, y):
        byte_index = y * bitmap.pitch + (x // 8)
        bit_mask = 0x80 >> (x & 7)
        return 1 if (bitmap.buffer[byte_index] & bit_mask) else 0

    elif RENDER_ENGINE in ("pillow_mono", "pillow_aa"):

      # ----- create temporary canvas -----
      img = Image.new("L", (size * 2, size * 2), 0)
      draw = ImageDraw.Draw(img)

      if DESCENDERS:
        draw.text((0, size // 4), chr(i), fill=255, font=font)
      else:
        draw.text((0, 0), chr(i), fill=255, font=font)

      bbox = img.getbbox()

      if bbox:
        img = img.crop(bbox)
        width, height = img.size
        pixels = img.load()
      else:
        width, height = 0, 0
        pixels = None

      if RENDER_ENGINE == "pillow_mono":
        def get_pixel(x, y):
          return 1 if pixels and pixels[x, y] > 0 else 0

      else:  # pillow_aa
        def get_pixel(x, y):
          return 1 if pixels and pixels[x, y] >= AA_THRESHOLD else 0

      # ----- fake FreeType metrics (approximation) -----
      xAdvance = width + PILLOW_EXTRA_SPACING
      xOffset = 0
      yOffset = -height + 1

    glyph_table.append({
      "xAdvance": xAdvance,
      "xOffset": xOffset,
      "yOffset": yOffset
    })

    # --------------------------------------------------
    # Bitmap storage type selection
    #
    # Glyphs are stored as 8/16/32-bit arrays to save space.
    # Each value represents ONE VERTICAL COLUMN.
    # --------------------------------------------------
    type_width = (height + 7) // 8
    if type_width == 0:
      type_width = 1
    if type_width == 3:
      type_width = 4  # align to 32-bit

    uint_size = type_width * 8

    # --------------------------------------------------
    # Output bitmap declaration
    # --------------------------------------------------
    ascii_code = i
    comment = f"   // 0x{ascii_code:02X}"

    if 32 <= ascii_code <= 126:
      comment += f" '{chr(ascii_code)}'"

    print(f"const uint{uint_size}_t {font_name}Char{i - first}[] = {{{comment}")

    # --------------------------------------------------
    # COLUMN-MAJOR BIT EXTRACTION
    #
    # Each output row is a vertical column:
    #   height = number of bits
    #   width  = number of values
    #
    # Bits are read bottom-to-top (IMPORTANT)
    # --------------------------------------------------
    for x in range(width):
      print("  0b", end="")

      for y in range(height - 1, -1, -1):
        if get_pixel(x, y):
          print("1", end="")
        else:
          print("0", end="")

      print("UL,")
      bytes_used += type_width

    print("};")

    # ----- Bitmap offset (not used further but kept for parity) -----
    bitmap_offset += (width * height + 7) // 8

  # --------------------------------------------------
  # Report memory usage (stderr)
  # --------------------------------------------------
  print(f"\n  {bytes_used} bytes used for bitmaps.", file=sys.stderr)

  # --------------------------------------------------
  # Output glyph table
  #
  # Stores:
  #   xAdvance, xOffset, yOffset, bitmap reference
  # --------------------------------------------------
  print(f"\nconst Glyph {font_name}Glyphs[] = {{")

  for i, g in enumerate(glyph_table):
    ascii_code = first + i

    line = f"  {{ {g['xAdvance']:3d}, {g['xOffset']:4d}, {g['yOffset']:4d}, GLYPHDATA({font_name}Char{i}) }}"

    if ascii_code < last:
      line += f",   // 0x{ascii_code:02X}"
      if 32 <= ascii_code <= 126:
        line += f" '{chr(ascii_code)}'"

    print(line)

  print(f" }}; // 0x{last:02X} '{chr(last)}'")

# --------------------------------------------------
# CLI MAIN ENTRY POINT
# --------------------------------------------------
def main():
  """
  Command line usage:

    python fontconvert.py font.ttf size [first] [last]
  """

  if len(sys.argv) < 3:
    print("Usage: python fontconvert.py fontfile size [first] [last]")
    sys.exit(1)

  font_path = sys.argv[1]
  size = int(sys.argv[2])

  if len(sys.argv) == 4:
    first = 32
    last = int(sys.argv[3])
  elif len(sys.argv) == 5:
    first = int(sys.argv[3])
    last = int(sys.argv[4])
  else:
    first, last = 32, 126

  # ----- Ensure valid range -----
  if last < first:
    first, last = last, first

  convert_font(font_path, size, first, last)

if __name__ == "__main__":
  main()
