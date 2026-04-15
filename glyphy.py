# version 56

# ==================================================
# GLYPHY – ProffieOS Text Font Analyzer & Renderer
# ==================================================
#        Version: 0.56 beta
#         Author: OlivierFlying747-8
#
# Looking for me? https://crucible.hubbe.net
#
#        License: GNU GPL-3.0
#
#         GitHub: https://github.com/olivierflying747-8/Glyphy
#           Docs: https://crucible.hubbe.net/t/project-glyphy-a-visualizer-validator-tool-for-proffieos-text-font-files/7777
#    Instalation: https://github.com/olivierflying747-8/Glyphy/blob/main/InstallationGuide/InstallationGuide.md
#  Report Errors: see Docs and/or Github
#
# ==================================================
# What this file does:
# - Parses a ProffieOS .h text font file (like Aurebesh10Font.h & StarJedi10Font.h)
# - Validates bitmap arrays and GLYPHDATA entries
# - Renders everything that can be found in your ProffieOS .h text font file
# - Detects structural and logical errors
# - Computes useful font metrics
# - Generates a readable analysis report
# - Includes tools to repair structural font issues
# ==================================================
# GLYPHY is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# ==================================================

"""
Quick start:
  python glyphy.py YourFont.h
"""
"""
▶ Running GLYPHY
Navigate to the folder containing glyphy.py (ProffieOS/display)
Right click on the "display" folder in left pane window (Windows Explorer)
Click on "Open command window here"
Run:
python glyphy.py Aurebesh10Font.h
  or
python glyphy.py LatoBlack6Font.h
  or
python glyphy.py Small5Font.h
  or
python glyphy.py StarJedi10Font.h
  or
python glyphy.py saber_logo.h
  or
...
"""

# ==================================================
# USER SETTINGS
# ==================================================

# --------------------------------------------------
# GLOBAL LAYOUT CONTROLS
# --------------------------------------------------

ROW_ALIGN             = "left"  # "left" / "center" / "right". Just for fun, because I can!
                                # I think it could be useful to generate cool .bmp logos.
                                # Must be "left" to match ProffieOS rendering exactly.

STRICT_PROFFIE_LAYOUT = True    # Emulate ProffieOS horizontal layout exactly (uses GLYPHDATA advance/x_offset exactly).
                                # Does NOT automatically force y_offset usage. Must be True to match ProffieOS rendering exactly.

EXTRA_GLYPH_SPACING   = 5       # Extra spacing added to GLYPHDATA advance when STRICT_PROFFIE_LAYOUT = False
                                # & when WIDTH_MODE is not "glyphdata".

USE_Y_OFFSET          = True    # Apply GLYPHDATA y_offset vertically. Must be True to match ProffieOS rendering exactly.
                                # Set False to ignore vertical offsets for debugging or logo design.

WIDTH_MODE = "glyphdata"        # Only used when STRICT_PROFFIE_LAYOUT = False
# "glyphdata"  → use GLYPHDATA advance-width only
# "bitmap"     → use bitmap width only
# "max"        → use max(bitmap, GLYPHDATA)

RENDER_MODE = "table"
# "table"      → to render the whole font.
# "text"       → to render a custom text string.
# "random"     → to render a glyph in a random .h file (not a font) for example saber_logo.h
# "this"       → to render THIS

CUSTOM_TEXT = ">h>e>l>l>o\n>t>h>e>r>e"
                              # If "text" is selected in RENDER_MODE, add your text here.
                              # ProffieOS "\n" is supported and will go to next line.
                              # If your text is too long to fit, it will wrap on multiple lines
                              # or get clipped depending on AUTO_WRAP.

AUTO_WRAP = True              # only meaningful when RENDER_MODE = "text"

LOOK_FOR = "saberLogoLS6"     # RENDER_MODE = "random"
                              # Name of the bitmap array to find & display in your random .h file.
                              # For example: from saber_logo.h
                              #              give "saberLogoLS6"

THIS = """
  0b11111111111100UL,
  0b10000000000100UL,
  0b10000000000111UL,
  0b10000000000101UL,
  0b10000000000111UL,
  0b10000000000100UL,
  0b11111111111100UL
  """                         # RENDER_MODE = "this"
                              # "THIS" is an example of a properly formatted ProffieOS glyph.
                              # Unfortunately Python cannot parse the ProffieOS format "{ 0bXXXUL }" because of
                              # the "UL" suffix, so a string literal (""" 0bXXXUL """) is used here instead.

DISPLAY_WIDTH = 128           # Width of displayable text (before scaling, not including borders) (capped at a minimum of 32)

# --------------------------------------------------
# Settings for single bitmap array rendering and/or custom text string (RENDER_MODE = "text", "random" or "this")
# --------------------------------------------------

DISPLAY_HEIGHT = 32               # (capped at a minimum of 32)
DISPLAY_HEIGHT_HARD_LIMIT = True  # Everything past DISPLAY_HEIGHT will be clipped
DO_BORDERS     = True             # Apply borders to single bitmap array rendering or custom text.

# --------------------------------------------------
# GEOMETRY
# --------------------------------------------------

OUTER_WHITE_BORDER = 2         # Outer white border thickness (capped at a minimum of 0)
INNER_BLACK_BORDER = 3         # Inner black border thickness (for diagnostic, a minimum of 2 is recommended) (capped at a minimum of 0)
SPACING            = 2         # Vertical spacing between rows (capped at a minimum of 0)

SCALE           = 4            # Image scaling factor for better visualization (capped at a minimum of 1)

ROTATION        = 0            # Accepted values: 0, 90 (for CW), -90 (for CCW), 180 or 270. For ProffieOS, your font should display correctly with 0.
FLIP_LEFT_RIGHT = False        # Mirror left to right (True or False). For ProffieOS, your font should display correctly with False.
FLIP_TOP_BOTTOM = False        # Mirror up to down (True or False). For ProffieOS, your font should display correctly with False.

LABEL_TTF       = "Arial.ttf"  # Name of the TTF font used for labels/legend if it can be found,
                               # otherwise the Python default TTF will be used.
LABEL_FONT_SIZE = 9            # choose between 8, 9 or 10
TTF_PATH        = r"C:\Windows\Fonts"
                               # Optional folder containing TTF fonts
                               # Typical system font folders:
                               # Windows : C:\Windows\Fonts
                               # macOS   : /System/Library/Fonts
                               #           /Library/Fonts
                               #           ~/Library/Fonts
                               # Linux   : /usr/share/fonts
                               #           /usr/local/share/fonts
                               #           ~/.fonts
                               #
                               # Example: TTF_PATH = r"C:\Windows\Fonts"
                               # Note for Windows: use r before the string

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

OUTPUT_FORMAT = "bmp"          # bmp / png / jpg — also (untested): gif / tiff / webp
OUTPUT_DIR = "glyphy_outputs"  # default output directory is "glyphy_outputs"

BLACK_AND_WHITE_ONLY   = False # Renders in bmp, without borders, scaling, diagnostic, legend or labels. ← ideal for creating bmp for oled
INVERT_BLACK_AND_WHITE = False # only applicable when BLACK_AND_WHITE_ONLY = True
BLACK_AND_WHITE_MODE   = "1"   # "1" for true black and white or "L" for levels of grey.

FILENAME_MODE = "iterate"      # Select "overwrite" to overwrite previously generated image or font report,
                               # select "iterate" to append _01.._99 before file extension.
                               # After _99, _00 will be created and overwritten continuously!
                               # Do you need more than 99 tests to fix your font?
FILENAME_ITERATE_RANGE = None  # Use 9, 99 or 999. Default is 99 ( = None )
AUTO_OPEN_IMAGE        = True  # Opens in your default image viewer
GENERATE_REPORT        = False # Create a .txt report about your font analysis.
FORCE_DETAILS          = True  # Adds character details regardless of errors/warnings detected.
AUTO_OPEN_REPORT       = True  # Opens in your default .txt viewer

OPEN_REPAIR_MENU       = False # Use at your own risk! It should only make changes to cloned fonts.
                               # Menu will only prompt to open, if errors are detected in your font.
                               # (errors such as: missing characters or wrong uintXX_t used)

# --------------------------------------------------
# Diagnostic controls
# --------------------------------------------------
SHOW_COMMENTED         = True   # Parse commented glyph arrays (True or False). ProffieOS will ignore commented bitmap glyphs.
SHOW_LABEL             = True   # Add a character label under your glyphs.
                                # Labels will only be shown in RENDER_MODE = "table".
LABEL_NUMBERING        = True   # Multiple glyph versions will get a number added to their labels
LABEL_INCREMENT        = False  # Label numbering will increment when True / decrement when False
LABEL_START            = 0      # Label start position (1 to start at 1 / 0 to start at 0)

DRAW_MISSING_BLOCK     = True   # To draw missing characters block (red)
FALLBACK_GLYPH_WIDTH   = 5      # Default width of missing characters

SHOW_GLYPH_ORIGIN      = False  # Add a purple vertical line where the glyph begins,
                                # only useful to detect the beginning of invisible glyph (like space and/or empty bitmaps)

DISPLAY_DIAGNOSTIC     = False  # Enable all Diagnostic controls as selected below
                                # (enable drawing of all Diagnostic controls at once or draw none).

VERTICAL_GRID_LINES        = True   # Vertical Grid lines (grey)
VERTICAL_GRID_MARKERS      = True   # Draw single pixel tick marks in top inner black border
VERTICAL_GRID_INTERVAL     = 16     # Draw ticks (and lines, after scaling) at 8,16,24,... pixels from left inner border in
                                    # the top border. (capped at a minimum of 2)
HORIZONTAL_GRID_LINES      = True   # Horizontal Grid lines (grey)
HORIZONTAL_GRID_MARKERS    = True   # Draw single pixel tick marks in left inner black border.
HORIZONTAL_GRID_INTERVAL   = 16     # Draw ticks (and lines, after scaling) at 16,32,48,... pixels from top inner border in
                                    # the left border. (capped at a minimum of 2)
SHOW_HORIZ_BASE_LINES      = True   # Horizontal Baseline lines (red)
DRAW_BASELINE_MARKER       = True   # Draw red baseline indicator on right border.
SHOW_HORIZ_CAP_DESC_LINES  = True   # Horizontal Cap-height (light-blue) & Descent lines (green)
DRAW_CAP_DESC_MARKERS      = True   # Draw light blue Cap-height and green Descent markers on right border.
VERTICAL_EDGE_LINE         = True   # Draw line on right edge to mark the end (red)
VERTICAL_EDGE_MARKER       = True   # Draw red tick on left side to mark the end.

SHOW_LEGEND                = True   # Add a legend area to the bottom of the rendered glyphs

# --------------------------------------------------
# Debug
# --------------------------------------------------
ENABLE_DEVELOPER_DEBUG_MODE = False # Adds additional debugging data to the report, the render and/or console output.
                                    # Also saves "ctx" to file, all 16.000+ lines of it.

FORCE_CORE_BREACH_EVENT     = False # See what happens when you turn this ON, I dare you!
                                    # Intended to only show when geometry is broken regardless of FORCE_CORE_BREACH_EVENT bool value.

# --------------------------------------------------
# Colors
# --------------------------------------------------

WHITE  = (255, 255, 255)  # used for outer border & text/font rendering
BLACK  = (  0,   0,   0)  # used for inner border, line spacing & background
RED    = (255,   0,   0)  # used for left edge & Baseline lines & missing characters (no GLYPHDATA or bitmap array entry)
BLUE   = (100, 200, 255)  # used for Cap_height (Ascent) lines
GREEN  = (  0, 255,   0)  # used for Descent lines
GREY   = (120, 120, 120)  # used for Grid lines & commented/duplicated bitmaps
YELLOW = (255, 255,   0)  # used for missing GLYPHDATA
ORANGE = (255, 140,   0)  # used for empty bitmaps
PURPLE = (160,  32, 240)  # used for SHOW_GLYPH_ORIGIN

# ==================================================
# END OF USER SETTINGS
# ==================================================

# ==================================================
# IMPORTANT INTERNAL RULES
# ==================================================
# - Glyphy never modifies bitmap art.
# - Repairs are best-effort structural fixes only.
# - Original files are never overwritten.
# - Repairs always create numbered clones.
# - Always review the generated clone before using it.
# ==================================================
# BITMAP FORMAT SPEC (DO NOT CHANGE)
# ==================================================
#
# Proffie bitmap format uses VERTICAL COLUMNS.
#
# Each value like:
#   0b00000000UL
#
# represents:
#   width  = 1 pixel
#   height = number of bits (8 here)
#
# Therefore:
#   bitmap_width  = number_of_values
#   bitmap_height = bit_length_of_each_value
#
# Example:
#   {0b11111111UL, 0b00011000UL}
#
#   width  = 2
#   height = 8
#
# This bitmap format is NOT row-based.
# DO NOT compute width from bit length.
# ==================================================

# For parser / fixer / auto-open:
import sys
import re
import os
import platform
import subprocess
import shutil
import threading
import time
# For renderer
from itertools import zip_longest
from PIL import Image, ImageDraw, ImageFont

if sys.stdout.encoding.lower() != "utf-8":
  sys.stdout.reconfigure(encoding="utf-8")

# ==============================================================================================================================

# ==================================================
# PARSE PROFFIE .h FONT FILE
# ==================================================

def parse_font_file(filename, dict_btmp_gdat):
  """
  Parse a ProffieOS .h font file and validate its structure.

  Responsibilities:
    1. Read Font File
    2. Build ctx / Context Dictionary
    3. Build Bitmap Dictionary / Extract Bitmap Arrays
    4. Build GLYPHDATA Dictionary / Extract GLYPHDATA
    5. Build Draw Pairs
    6. Glyph Processing Loop
    7. Produce Font Metric
    8. Produce Diagnostics for Reporting & Fix-it Menu

  Returns:
    dict containing:
      - glyph_records
      - report_details
      - metrics
      - diagnostics
      - severity_totals

  Side Effects:
    - Generates a human-readable analysis report file.

  run_repair_menu(font_file, ctx) can reuse diagnostics to repair files.

  IMPORTANT BITMAP RULE

  Each bitmap value (0bXXXXXXXXUL) is ONE VERTICAL COLUMN.

  height = bit length
  width  = number of values

  Example:
    0b00000000UL -> width 1, height 8

  Never treat rows as horizontal pixels.
  """

  # ----- precompiled regex (speed + clarity) -----
  RE_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
  RE_LINE_COMMENT  = re.compile(r"//.*")
  RE_BINARY_ROW    = re.compile(r"^[01]+$")              # this will accept "0b01010101UL ,"
  RE_BINARY_SPACE  = re.compile(r"[01]\s+[01]")

  # ==================================================
  # PHASE 1 — LOAD FILE
  # ==================================================

  with open(filename, "r", encoding="utf-8") as f:
    raw_content = f.read()

  # ----- build comment ranges (for precise commented detection) -----
  comment_ranges = []

  for m in RE_BLOCK_COMMENT.finditer(raw_content):
    comment_ranges.append((m.start(), m.end()))

  for m in RE_LINE_COMMENT.finditer(raw_content):
    comment_ranges.append((m.start(), m.end()))

  def is_position_commented(pos, ranges):
    for start, end in ranges:
      if start <= pos < end:
        return True
    return False

  # remove comments for active-content parsing
  content_no_comments = RE_BLOCK_COMMENT.sub("", raw_content)
  content_no_comments = RE_LINE_COMMENT.sub("", content_no_comments)

  # ==================================================
  # PHASE 2 — BUILD ctx CONTEXT DICTIONARY
  # ==================================================

  ctx = {
    "filename": filename,
    "raw_content": raw_content,
    "content_no_comments": content_no_comments,

    "bitmap_dict": {},
    "glyphdata_dict": {},

    "glyph_records": [],
    "report_details": [],
    "char_reports": [],

    "metrics": {},
    "diagnostics": {},

    "severity_totals": {
      "critical": 0,
      "error": 0,
      "warning": 0,
      "info": 0
    }
  }

  # ==================================================
  # PHASE 3 — BUILD BITMAP DICTIONARY
  # ==================================================

  bitmap_matches = list(re.finditer(
    r"const\s+uint(\d+)_t\s+(\w+Char(\d+))\s*\[\]\s*=\s*\{([\s\S]*?)\};",
    raw_content,
    re.DOTALL
  ))

  for match in bitmap_matches:
    uint_declared, full_name, index, body = match.groups()

    index = int(index)
    version = {
      "body": body,
      "uint_declared": int(uint_declared),
      "is_commented": is_position_commented(match.start(), comment_ranges),
      "full_name": full_name,
      "line": raw_content.count("\n", 0, match.start()) + 1
    }

    ctx["bitmap_dict"].setdefault(index, []).append(version)

  # ==================================================
  # PHASE 4 — BUILD GLYPHDATA DICTIONARY
  # ==================================================

  glyphdata_matches = list(re.finditer(
    r"\{\s*(\d+),\s*(-?\d+),\s*(-?\d+),\s*GLYPHDATA\((\w+Char(\d+))\)",
    raw_content
  ))

  for match in glyphdata_matches:
    advance_width, x_offset, y_offset, full_name, index = match.groups()
    index = int(index)
    version = {
      "advance_width": int(advance_width),
      "x_offset": int(x_offset),
      "y_offset": int(y_offset),
      "is_commented": is_position_commented(match.start(), comment_ranges),
      "name": full_name,
      "line": raw_content.count("\n", 0, match.start()) + 1
    }

    ctx["glyphdata_dict"].setdefault(index, []).append(version)

  # ==================================================
  # PHASE 5 — BUILD DRAW PAIRS
  # ==================================================

  def build_draw_pairs(bitmap_versions, glyphdata_versions):

    """
    Build deterministic bitmap/GLYPHDATA pairs.

    Ensures Renderer draws:
      - every active version
      - then every commented version
      - even when bitmap or glyphdata is missing

    Returns list of pairs.
    """

    pairs = []
    active_bitmap       = [b for b in bitmap_versions if not b["is_commented"]]
    commented_bitmap    = [b for b in bitmap_versions if b["is_commented"]]
    active_glyphdata    = [gdata for gdata in glyphdata_versions if not gdata["is_commented"]]
    commented_glyphdata = [gdata for gdata in glyphdata_versions if gdata["is_commented"]]

    # ----- active pairs -----
    if not active_bitmap and not active_glyphdata:
      if DRAW_MISSING_BLOCK:
        pairs.append({
          "bitmap": None,
          "glyphdata": None,
          "commented": False,
          "duplicate": False
        })
    else:
      for pair_index, (bitmap, gdata) in enumerate(zip_longest(active_bitmap, active_glyphdata)):
        pairs.append({
          "bitmap": bitmap,
          "glyphdata": gdata,
          "commented": False,
          "duplicate": pair_index > 0
        })

    # ----- commented pairs -----
    for pair_index, (bitmap, gdata) in enumerate(zip_longest(commented_bitmap, commented_glyphdata)):
      pairs.append({
        "bitmap": bitmap,
        "glyphdata": gdata,
        "commented": True,
        "duplicate": True
      })

    return pairs

  # ==================================================
  # PHASE 6 — GLYPH PROCESSING LOOP
  # ==================================================

  total_found = 0
  total_errors = 0
  total_critical = 0
  total_error = 0
  total_warning = 0
  total_info = 0

  # ----- PRIMARY VERSION SELECTION -----
  def select_primary_version(versions):
    for v in versions:
      if not v["is_commented"]:
        return v
    return versions[0] if versions else None

  # --------------------------------------------------
  # VALIDATION LOOP (char0 → char94)
  # --------------------------------------------------
  for char_index in range(95): # 32 ... 126

    bitmap_versions = ctx["bitmap_dict"].get(char_index, [])
    glyphdata_versions = ctx["glyphdata_dict"].get(char_index, [])
    active_bitmap_versions = [ v for v in bitmap_versions if not v["is_commented"] ]
    active_glyphdata_versions = [ v for v in glyphdata_versions if not v["is_commented"] ]
    primary_bitmap = select_primary_version(bitmap_versions)
    primary_glyphdata = select_primary_version(glyphdata_versions)
    has_bitmap = primary_bitmap is not None
    has_glyphdata = primary_glyphdata is not None
    pairs = build_draw_pairs(bitmap_versions, glyphdata_versions)
    errors = []
    char_critical = False

    # --------------------------------------------------
    # VERSION COMPOSITION ANALYSIS
    # --------------------------------------------------
    active_bitmap_count = sum(1 for v in bitmap_versions if not v["is_commented"])
    commented_bitmap_count = len(bitmap_versions) - active_bitmap_count
    active_glyphdata_count = sum(1 for v in glyphdata_versions if not v["is_commented"])
    commented_glyphdata_count = len(glyphdata_versions) - active_glyphdata_count

    # ----- Completely missing -----
    if not (has_bitmap or has_glyphdata):
      errors.append("[ERROR] completely missing glyph definition (no bitmap, no GLYPHDATA)")
      char_critical = True

    else:
      total_found += 1

    # ----- bitmap version mishmash analysis -----
    if active_bitmap_count == 0 and commented_bitmap_count > 0:
      lines = [str(v["line"]) for v in bitmap_versions]
      errors.append(f"[ERROR] bitmap only exists commented out ({commented_bitmap_count} commented,")
      errors.append(f"  lines: {', '.join(lines)})")
      char_critical = True

    elif active_bitmap_count > 1:
      active_lines = [str(v["line"]) for v in bitmap_versions if not v["is_commented"]]
      commented_lines = [str(v["line"]) for v in bitmap_versions if v["is_commented"]]
      # I know, I know. It should say "mismatched" but I like "mishmash" better!
      errors.append(f"[ERROR] bitmap definition mishmash ({active_bitmap_count} active + {commented_bitmap_count} commented")
      errors.append(f"  active lines: {', '.join(active_lines)}; commented lines: {', '.join(commented_lines)})")
      char_critical = True

    elif active_bitmap_count == 1 and commented_bitmap_count > 0:
      commented_lines = [str(v["line"]) for v in bitmap_versions if v["is_commented"]]
      errors.append(f"[INFO] bitmap has historical versions: 1 active + {commented_bitmap_count} commented")
      errors.append(f"  lines: {', '.join(commented_lines)}")

    # ----- GLYPHDATA version mishmash analysis -----
    if active_glyphdata_count == 0 and commented_glyphdata_count > 0:
      lines = [str(v["line"]) for v in glyphdata_versions]
      errors.append(f"[ERROR] GLYPHDATA only exists commented out ({commented_glyphdata_count} commented")
      errors.append(f"  lines: {', '.join(lines)}")
      char_critical = True

    elif active_glyphdata_count > 1:
      active_lines = [str(v["line"]) for v in glyphdata_versions if not v["is_commented"]]
      commented_lines = [str(v["line"]) for v in glyphdata_versions if v["is_commented"]]
      errors.append(f"[ERROR] GLYPHDATA definition mishmash ({active_glyphdata_count} active + {commented_glyphdata_count} commented")
      errors.append(f"  active lines: {', '.join(active_lines)}; commented lines: {', '.join(commented_lines)}")
      char_critical = True

    elif active_glyphdata_count == 1 and commented_glyphdata_count > 0:
      commented_lines = [str(v["line"]) for v in glyphdata_versions if v["is_commented"]]
      errors.append(f"[INFO] GLYPHDATA has historical versions: 1 active + {commented_glyphdata_count} commented")
      errors.append(f"  lines: {', '.join(commented_lines)}")

    # --------------------------------------------------
    # BITMAP EXTRACTION
    # --------------------------------------------------
    bitmap_height = 0
    bitmap_width = 0
    if has_bitmap:
      for version in bitmap_versions:
        rows = []
        body = version["body"]

        # --------------------------------------------------
        # BITMAP ROW EXTRACTION
        # --------------------------------------------------

        # ----- remove comments inside bitmap body -----
        clean_body = RE_LINE_COMMENT.sub("", RE_BLOCK_COMMENT.sub("", body))

        # ----- detect empty bitmap (whitespace-only counts as empty) -----
        if not clean_body.strip():
          tokens = []
        else:
          binary_matches = re.findall(r"0b[01]+UL", clean_body)

          # ----- detect missing comma between multiple binary rows -----
          if len(binary_matches) > 1:
            # ----- collapse whitespace to detect separation without commas -----
            normalized = re.sub(r"\s+", " ", clean_body.strip())

            if "," not in normalized:
              errors.append("[ERROR] bitmap rows must be comma-separated")
              errors.append(f"  line: {version['line']}")

          tokens = clean_body.split(",")

        for token in tokens:
          token = token.strip()
          if not token:
            continue

          # ----- remove UL suffix -----
          token = token.replace("UL", "")

          # ----- remove 0b prefix -----
          if token.startswith("0b"):
            token = token[2:]

          # ----- validate binary -----
          if not RE_BINARY_ROW.fullmatch(token):
            errors.append(f"[ERROR] invalid binary row '{token}'")
            errors.append(f"  line: {version['line']}")
            continue

          rows.append(token)

        # ----- bitmap dimensions -----
        version["bitmap_height"] = max(len(r) for r in rows) if rows else 0
        version["bitmap_width"] = len(rows)
        bitmap_height = version["bitmap_height"]
        bitmap_width = version["bitmap_width"]

        # FORMAT INVARIANT: bitmap values are vertical columns
        assert version["bitmap_width"] == len(rows), "Width must equal number of bitmap values"

        # --------------------------------------------------
        # RECTANGLE VALIDATION (bitmap blocks should look rectangular)
        # --------------------------------------------------
        if not rows:
          errors.append("[INFO] bitmap contains no binary rows / bitmap is empty")
          errors.append(f"  line: {version['line']}")

        unique = sorted({len(r) for r in rows})

        if len(unique) > 1:
          errors.append(f"[WARNING] bitmap is not rectangular (row lengths: {unique})")
          errors.append(f"  line: {version['line']}")
          #errors.append("  suggestion: add or remove zeros to make rows equal")

          # ----- determine target length -----
          max_length = max(unique)
          min_length = min(unique)

          # ----- check if longest rows can be safely trimmed -----
          can_trim = True

          for row_bits in rows:
            if len(row_bits) == max_length:
              extra_bits = row_bits[min_length:]

              if not all(bit == '0' for bit in extra_bits):
                can_trim = False
                break

          # ----- choose normalization strategy -----
          if can_trim:
            target_length = min_length
          else:
            target_length = max_length

          # ----- helper: number → word -----
          number_words = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            11: "eleven",
            12: "twelve",
            13: "thirteen",
            14: "fourteen",
            15: "fifteen",
            16: "sixteen",
            17: "seventeen",
            18: "eighteen",
            19: "nineteen",
            20: "twenty"
          }

          def number_to_word(number):
            return number_words.get(number, str(number))

          # ----- grouping containers -----
          add_zero_groups = {}     # key = diff, value = list of row numbers
          remove_zero_groups = {}  # key = diff, value = list of row numbers

          # ----- analyze rows -----
          for row_index, row_bits in enumerate(rows):
            row_length = len(row_bits)

            # ----- Case 1: shorter rows → pad -----
            if row_length < target_length:
              difference = target_length - row_length
              add_zero_groups.setdefault(difference, []).append(row_index + 1)

            # ----- Case 2: longer rows → trim ONLY if safe -----
            elif row_length > target_length:
              extra_bits = row_bits[target_length:]

              if all(bit == '0' for bit in extra_bits):
                difference = row_length - target_length
                remove_zero_groups.setdefault(difference, []).append(row_index + 1)

          # ----- helper: format row list -----
          def format_row_list(row_numbers):
            if len(row_numbers) == 1:
              return f"row {row_numbers[0]}"
            else:
              return "rows " + ", ".join(map(str, row_numbers))

          # ----- emit grouped suggestions -----
          for difference, row_numbers in sorted(add_zero_groups.items()):
            word = number_to_word(difference)
            plural = "" if difference == 1 else "s"
            row_text = format_row_list(row_numbers)
            errors.append(f"  suggestion: add {word} trailing zero{plural} to {row_text}")

          for difference, row_numbers in sorted(remove_zero_groups.items()):
            word = number_to_word(difference)
            plural = "" if difference == 1 else "s"
            row_text = format_row_list(row_numbers)
            errors.append(f"  suggestion: delete {word} trailing zero{plural} from {row_text}")

        # --------------------------------------------------
        # UINT VALIDATION
        # --------------------------------------------------
        if rows:

          # ----- bitmap height -----
          height = version["bitmap_height"]
          declared = version["uint_declared"]

          if height <= 8:
            required = 8
          elif height <= 16:
            required = 16
          elif height <= 32:
            required = 32
          else:
            required = 64

          # ----- store correct uint for repair system -----
          version["correct_uint"] = required

          # ----- Invalid uint type -----
          if declared not in (8, 16, 32):
            errors.append(f"[WARNING] Invalid uint type uint{declared}_t (must be uint8_t, uint16_t or uint32_t)")
            errors.append(f"  line: {version['line']}")
            errors.append(f"  suggestion: replace uint{declared}_t with uint{required}_t")
            char_critical = True

          # ----- too small -----
          if declared < required:
            errors.append(f"[ERROR] uint{declared}_t TOO SMALL (needs at least {height} bits)")
            errors.append(f"  line: {version['line']}")
            errors.append(f"  suggestion: replace uint{declared}_t with uint{required}_t")
            char_critical = True

          # ----- too large -----
          elif declared > required:
            errors.append(f"[INFO] uint{declared}_t larger than necessary (max used {height} bits)")
            errors.append(f"  line: {version['line']}")
            errors.append(f"  suggestion: replace uint{declared}_t with uint{required}_t")

          if height > 32:
            errors.append(f"[WARNING] bitmap is too tall ({height}), it will not fit on a 32px OLED (it will be clipped)")
            errors.append(f"  line: {version['line']}")

    # --------------------------------------------------
    # GLYPHDATA VALIDATION
    # --------------------------------------------------

    def validate_bitmap_vs_advance(
      bitmap_width,
      advance_width,
      x_offset,
      y_offset,
      glyph_line,
      errors
    ):

      # ----- skip spatial validation for empty bitmap -----
      if bitmap_width == 0:
        return

      bitmap_left = x_offset
      bitmap_right = x_offset + bitmap_width

      # ----- Case 1 — advance width is zero but bitmap exists -----
      if advance_width == 0 and bitmap_width > 0:
        errors.append(f"[INFO] advance width is zero but bitmap contains visible pixels, width ({bitmap_width})")
        errors.append(f"  line: {glyph_line}")
        errors.append(f"  suggestion: replace '{{{advance_width}, {x_offset}, {y_offset}}}' with '{{{bitmap_width}, {x_offset}, {y_offset}}}'")

      # ----- Case 2 — advance width smaller than bitmap -----
      elif advance_width < bitmap_width:
        errors.append(f"[INFO] advance width ({advance_width}) smaller than bitmap width ({bitmap_width})")
        errors.append(f"  line: {glyph_line}")
        errors.append(f"  suggestion: replace '{{{advance_width}, {x_offset}, {y_offset}}}' with '{{{bitmap_width}, {x_offset}, {y_offset}}}'")

      # ----- Case 3 — bitmap lies completely outside advance box -----
      if bitmap_right <= 0 or bitmap_left >= advance_width:
        errors.append("[INFO] bitmap lies completely outside advance width box")
        errors.append(f"  line: {glyph_line}")
        #errors.append("  suggestion: check x_offset and advance_width values")
        errors.append(f"  note: bitmap spans [{bitmap_left}, {bitmap_right}] while advance width is [0, {advance_width}]")
        if advance_width == 0:
          errors.append("  note: advance width is zero, so bitmap will not advance cursor (this may be intentional)"  )
        elif bitmap_right <= 0:
          errors.append("  note: bitmap is entirely left of the drawing origin (this may be intentional)")
          errors.append("  suggestion: increase advance_width or increase x_offset to shift it right")
        elif bitmap_left >= advance_width:
          errors.append("  note: bitmap starts beyond the advance width (this may be intentional)")
          errors.append("  suggestion: decrease x_offset or increase advance_width to bring it into range")

    if has_bitmap and has_glyphdata:
      B = len(bitmap_versions)
      G = len(glyphdata_versions)

      # ----- Case 1: 1 bitmap, multiple glyphdata -----
      if B == 1 and G > 1:
        bitmap_width = bitmap_versions[0]["bitmap_width"]
        for glyphdata_version in glyphdata_versions:
          advance_width = glyphdata_version["advance_width"]
          x_offset = glyphdata_version["x_offset"]
          y_offset = glyphdata_version["y_offset"]
          glyph_line = glyphdata_version["line"]

          validate_bitmap_vs_advance(
            bitmap_width,
            advance_width,
            x_offset,
            y_offset,
            glyph_line,
            errors
          )

      # ----- Case 2: multiple bitmap, 1 glyphdata -----
      elif G == 1 and B > 1:
        glyphdata = glyphdata_versions[0]
        advance_width = glyphdata["advance_width"]
        x_offset = glyphdata["x_offset"]
        y_offset = glyphdata["y_offset"]
        for bitmap in bitmap_versions:
          bitmap_width = bitmap["bitmap_width"]
          glyph_line = active_glyphdata_versions[0]["line"] if active_glyphdata_versions else None

          validate_bitmap_vs_advance(
            bitmap_width,
            advance_width,
            x_offset,
            y_offset,
            glyph_line,
            errors
          )

      # ----- Case 3 & 4: equal or mismatched multiples -----
      else:
        pair_count = min(B, G)
        for i in range(pair_count):
          bitmap_width = bitmap_versions[i]["bitmap_width"]
          glyphdata = glyphdata_versions[i]
          advance_width = glyphdata["advance_width"]
          x_offset = glyphdata["x_offset"]
          y_offset = glyphdata["y_offset"]
          glyph_line = active_glyphdata_versions[0]["line"] if active_glyphdata_versions else None

          validate_bitmap_vs_advance(
            bitmap_width,
            advance_width,
            x_offset,
            y_offset,
            glyph_line,
            errors
          )

        if B > pair_count:
          extra_lines = [str(v["line"]) for v in bitmap_versions[pair_count:]]
          errors.append(f"[INFO] {B - pair_count} bitmap version(s) have no matching glyphdata")
          errors.append(f"  lines: {', '.join(extra_lines)}")

        if G > pair_count:
          extra_lines = [str(v["line"]) for v in glyphdata_versions[pair_count:]]
          errors.append(f"[INFO] {G - pair_count} glyphdata version(s) have no matching bitmap")
          errors.append(f"  lines: {', '.join(extra_lines)}")

    if FORCE_DETAILS:
      note_lines = []

      # ----- REAL (measured) bitmap -----
      real_height = bitmap_height if has_bitmap else 0
      real_width = bitmap_width if has_bitmap else 0

      # ----- DECLARED height (uintXX_t) -----
      declared_height = None
      if primary_bitmap:
        declared_height = primary_bitmap.get("uint_declared")

      # ----- GLYPHDATA -----
      if primary_glyphdata:
        y_offset = primary_glyphdata["y_offset"]
        x_offset = primary_glyphdata["x_offset"]
        declared_width = primary_glyphdata["advance_width"]
      else:
        y_offset = None
        declared_width = None

      # ----- format nicely -----
      note_lines.append(f"[NOTE] height: {real_height}px (declared max: {declared_height}) width: {real_width}px (advance: {declared_width})")
      note_lines.append(f"     y_offset: {y_offset}                  x_offset: {x_offset}")

      # ----- inject at TOP of errors -----
      errors = note_lines + errors

    # ----- severity counting -----
    char_error_count = 0
    char_warning_count = 0
    char_info_count = 0
    char_note_count = 0

    for msg in errors:
      if msg.startswith("[ERROR]"):
        char_error_count += 1
        total_error += 1
      elif msg.startswith("[WARNING]"):
        char_warning_count += 1
        total_warning += 1
      elif msg.startswith("[INFO]"):
        char_info_count += 1
        total_info += 1
      elif msg.startswith("[NOTE]"):
        char_note_count += 1

    if char_critical:
      total_critical += 1

    # --------------------------------------------------
    # BUILD GLYPH RECORD
    # --------------------------------------------------
    ctx["glyph_records"].append({

      "ascii_code": char_index + 32,
      "char": chr(char_index + 32),
      "bitmap_versions": bitmap_versions,
      "glyphdata_versions": glyphdata_versions,
      "primary_bitmap": primary_bitmap,
      "primary_glyphdata": primary_glyphdata,
      "draw_pairs": pairs,
      "effective_height": bitmap_height,
      "validation": errors,
      # ----- Renderer compatibility -----
      "status_flags": {
        "missing_bitmap": not has_bitmap,
        "missing_glyphdata": not has_glyphdata,
        "duplicate_bitmap": len(active_bitmap_versions) > 1,
        "duplicate_glyphdata": len(active_glyphdata_versions) > 1,
        "commented_bitmap_only": (
          bool(bitmap_versions) and
          all(v["is_commented"] for v in bitmap_versions)
        ),
        "commented_glyphdata_only": (
          bool(glyphdata_versions) and
          all(v["is_commented"] for v in glyphdata_versions)
        )
      }
    })

    ctx["char_reports"].append({
      "index": char_index,
      "critical": char_critical,
      "errors": errors,
      "error_count": char_error_count,
      "warning_count": char_warning_count,
      "info_count": char_info_count,
      "note_count": char_note_count
    })

    if errors:
      total_errors += 1
      ctx["report_details"].append(f"char{char_index} - '{chr(char_index+32)}':")
      for e in errors:
        ctx["report_details"].append("  " + e)
      ctx["report_details"].append("")

  # ==================================================
  # PHASE 7 — FONT METRICS
  # ==================================================

  bitmap_widths = []
  bitmap_heights = []
  advance_widths = []
  x_offsets = []
  y_offsets = []
  max_height = 0
  max_height_char = None
  max_descent = 0
  max_descent_char = None
  widest_bitmap_width = 0
  widest_bitmap_char = None
  widest_advance_width = 0
  widest_advance_char = None

  for glyph in ctx["glyph_records"]:
    primary_bitmap = glyph["primary_bitmap"]
    primary_glyphdata = glyph["primary_glyphdata"]
    if not primary_bitmap or not primary_glyphdata:
      continue

    # ----- Use previously computed height -----
    bitmap_height = glyph["effective_height"]

    bitmap_width = primary_bitmap["bitmap_width"]
    advance_width = primary_glyphdata["advance_width"]
    x_offset = primary_glyphdata["x_offset"]
    y_offset = primary_glyphdata["y_offset"]
    if bitmap_width is not None:
      bitmap_widths.append(bitmap_width)
    if bitmap_height is not None:
      bitmap_heights.append(bitmap_height)
    if advance_width is not None:
      advance_widths.append(advance_width)
    if x_offset is not None:
      x_offsets.append(x_offset)
    if y_offset is not None:
      y_offsets.append(y_offset)

    # ----- Tallest glyph -----
    if bitmap_height > max_height:
      max_height = bitmap_height
      max_height_char = f"char{glyph['ascii_code']-32} - '{chr(glyph['ascii_code'])}'"

    # ----- Largest descent -----
    if y_offset + height > max_descent:
      max_descent = y_offset + height
      max_descent_char = f"char{glyph['ascii_code']-32} - '{chr(glyph['ascii_code'])}'"

    # ----- Widest bitmap glyph -----
    if bitmap_width > widest_bitmap_width:
      widest_bitmap_width = bitmap_width
      widest_bitmap_char = f"char{glyph['ascii_code']-32} - '{chr(glyph['ascii_code'])}'"

    # ----- Widest advance glyph -----
    if advance_width > widest_advance_width:
      widest_advance_width = advance_width
      widest_advance_char = f"char{glyph['ascii_code']-32} - '{chr(glyph['ascii_code'])}'"

  # ----- Average widths -----
  average_bitmap_width = int(sum(bitmap_widths) / len(bitmap_widths) + 0.5) if bitmap_widths else 0
  average_advance_width = int(sum(advance_widths) / len(advance_widths) + 0.5) if advance_widths else 0
  average_x_offset = int(sum(x_offsets) / len(x_offsets) + 0.5) if x_offsets else 0

  # ----- Average heights -----
  average_bitmap_height = int(sum(bitmap_heights) / len(bitmap_heights) + 0.5) if bitmap_heights else 0
  average_y_offset = int(sum(y_offsets) / len(y_offsets) + 0.5) if y_offsets else 0

  ctx["metrics"] = {
    "average_bitmap_width": average_bitmap_width,
    "average_bitmap_height": average_bitmap_height,
    "average_advance_width": average_advance_width,
    "average_x_offset": average_x_offset,
    "average_y_offset": average_y_offset,
    "widest_bitmap_char": widest_bitmap_char,
    "widest_bitmap_width": widest_bitmap_width,
    "max_height_char": max_height_char,
    "max_height": max_height,
    "widest_advance_char": widest_advance_char,
    "widest_advance_width": widest_advance_width,
    "max_descent_char": max_descent_char,
    "max_descent": max_descent
  }

  # ==================================================
  # PHASE 8 — DIAGNOSTIC AGGREGATION
  # ==================================================

  total_missing_characters = 0
  total_missing_bitmap = 0
  total_missing_glyphdata = 0
  total_commented_bitmap_only = 0
  total_commented_glyphdata_only = 0
  total_duplicate_bitmap = 0
  total_duplicate_glyphdata = 0

  for glyph in ctx["glyph_records"]:
    flags = glyph.get("status_flags", {})

    if flags["missing_bitmap"] and flags["missing_glyphdata"]:
      total_missing_characters += 1

    if flags["missing_bitmap"]:
      total_missing_bitmap += 1

    if flags["missing_glyphdata"]:
      total_missing_glyphdata += 1

    if flags["commented_bitmap_only"]:
      total_commented_bitmap_only += 1

    if flags["commented_glyphdata_only"]:
      total_commented_glyphdata_only += 1

    if flags["duplicate_bitmap"]:
      total_duplicate_bitmap += 1

    if flags["duplicate_glyphdata"]:
      total_duplicate_glyphdata += 1

  ctx["diagnostics"] = {
      "total_found": total_found,
      "total_errors": total_errors,
      "total_bg_errors": {"enabled":False,"details":dict_btmp_gdat},
      "total_critical_chars": total_critical,
      "total_missing_characters": total_missing_characters,
      "total_missing_bitmap": total_missing_bitmap,
      "total_missing_glyphdata": total_missing_glyphdata,
      "total_commented_bitmap_only": total_commented_bitmap_only,
      "total_commented_glyphdata_only": total_commented_glyphdata_only,
      "total_duplicate_bitmap": total_duplicate_bitmap,
      "total_duplicate_glyphdata": total_duplicate_glyphdata
  }

  ctx["severity_totals"] = {
      "critical": total_critical,
      "error": total_error,
      "warning": total_warning,
      "info": total_info
  }

  return ctx

# ===============================
# LOAD TTF FONT
# ===============================

def load_label_font():
  """
  Load font used for glyph labels & legend.
  Returns (font, font_height, font_size, font_path_used)
  """

  font_path_used = None
  font = None
  font_size = max(8, min(10, LABEL_FONT_SIZE))

  # --------------------------------------------------
  # Internal helper: find font in system directories
  # --------------------------------------------------

  def find_system_font(font_name):

    system = platform.system()
    search_paths = []

    if system == "Windows":
      # ----- Use WINDIR environment variable (correct Windows way) -----
      windir = os.environ.get("WINDIR")
      if windir:
        search_paths.append(os.path.join(windir, "Fonts"))
      else:
        search_paths.append(r"C:\Windows\Fonts")

    elif system == "Darwin":  # macOS
      search_paths = [
        "/System/Library/Fonts",
        "/Library/Fonts",
        os.path.expanduser("~/Library/Fonts")
      ]

    else:  # Linux
      search_paths = [
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        os.path.expanduser("~/.fonts"),
        os.path.expanduser("~/.local/share/fonts")
      ]

    # ----- fast direct lookup first -----
    for base in search_paths:
      candidate = os.path.join(base, font_name)
      if os.path.exists(candidate):
        return candidate

    # ----- slower recursive search if needed -----
    for base in search_paths:
      if not os.path.exists(base):
        continue
      for root, _, files in os.walk(base):
        if font_name in files:
          return os.path.join(root, font_name)

    return None

  # ----- User provided font (full path) -----
  if LABEL_TTF:
    try:
      if TTF_PATH:
        full_path = os.path.join(TTF_PATH, LABEL_TTF)
      else:
        full_path = find_system_font(LABEL_TTF) or LABEL_TTF
      font = ImageFont.truetype(full_path, font_size)
      font_path_used = full_path
    except:
      font = None

  # ----- System fallback -----
  if font is None:
    for name in ("DejaVuSans.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"):
      try:
        if TTF_PATH:
          full_path = os.path.join(TTF_PATH, name)
        else:
          full_path = find_system_font(name) or name
        font = ImageFont.truetype(full_path, font_size)
        font_path_used = full_path
        break
      except:
        continue

  # ----- Final guaranteed fallback -----
  if font is None:
    font = ImageFont.load_default()
    font_path_used = "PIL default"

  # ----- Measure height using safe string -----
  bbox = font.getbbox("Ag")
  font_height = bbox[3] - bbox[1]

  return font, font_height, font_size, font_path_used

# ==================================================
# BAD MF OVERLORD
# ==================================================

GET_BTMP_GDAT = object() # sentinel
GEOMETRY_TAMPERED = False
def report_geometry_correction():
  global GEOMETRY_TAMPERED
  GEOMETRY_TAMPERED = True

# ==================================================
# BAD MF
# ==================================================

def inner_core_critical_hit(img_mode):
  """
  Core Breach Event visual overlay.
  """

  dict_btmp_gdat = None

  # ---------------------------------------------
  # Fragmented checksum payload assembly
  # ---------------------------------------------
  fragments = [
    0x444f4e27, 0x54204d45, 0x53530a57,
    0x49544820, 0x474c5950, 0x48592773,
    0x0a47454f, 0x4d455452, 0x59000000,
  ]

  # ----- fragments reality check -----
  def enforce_fragment_integrity_barrier(frags):
    acc = 0xA5A5A5A5
    mix = 0xC3C3C3C3
    for i, f in enumerate(fragments):
      acc ^= ((f << (i % 5)) | (f >> (32 - (i % 5)))) & 0xffffffff
      mix = (mix + f * (i + 1)) & 0xffffffff
      mix ^= (mix << 7) & 0xffffffff
      mix ^= (mix >> 11)
    if ((acc ^ mix) & 0xFFFF) == 0:
      acc ^= 0xDEADBEEF
    return acc ^ mix

  if img_mode is GET_BTMP_GDAT:
    integrity = enforce_fragment_integrity_barrier(fragments)

    dict_btmp_gdat = {
        "integrity": integrity,
        "fragments": fragments,
        "validity": (integrity * 2654435761) & 0xFFFFFFFF,
        "phase": ((integrity >> 3) ^ 0xA5A5A5A5) & 0xFFFFFFFF
    }

    return None, dict_btmp_gdat

  global OUTER_WHITE_BORDER, INNER_BLACK_BORDER
  global SCALE, DISPLAY_WIDTH, DISPLAY_HEIGHT
  global SPACING, SHOW_HORIZ_BASE_LINES
  global GEOMETRY_TAMPERED, FORCE_CORE_BREACH_EVENT

  img = img_mode

  trigger = GEOMETRY_TAMPERED or FORCE_CORE_BREACH_EVENT
  if not trigger:
    return img, None

  USE_ENHANCED_LIGHTNING  = True
  USE_ENHANCED_HYPERSPACE = True
  FUZZY_TEXT              = False # <-- I don't like it fuzzy!
  # ----- Core breach must render in color -----
  if img.mode != "RGBA":
    img = img.convert("RGBA")

  # ----- big endian assembly -----
  raw_bytes = b"".join(f.to_bytes(4, "big") for f in fragments)
  payload = raw_bytes.rstrip(b"\x00").decode("utf-8")
  lines = payload.split("\n")

  import random
  import math
  draw = ImageDraw.Draw(img)
  rng = random.Random(1337)

  # ---------------------------------------------
  # Borders and circle geometry
  # ---------------------------------------------
  BORDERS = OUTER_WHITE_BORDER + INNER_BLACK_BORDER
  if BORDERS < 2:
    BORDERS = 2

  if BLACK_AND_WHITE_ONLY:
    BORDERS = 1

  render_width = img.width - (BORDERS * 2)
  render_height = img.height - (BORDERS * 2)
  center_x = BORDERS + render_width // 2
  center_y = BORDERS + render_height // 2

  outer_radius = min(render_width, render_height) // 2
  inner_radius = outer_radius - 4  # change gap between red rings

  # ---------------------------------------------
  # Darkening veil
  # ---------------------------------------------
  SHOW_HORIZ_BASE_LINES = False
  veil_layer = img.copy().convert("RGBA")
  veil_draw = ImageDraw.Draw(veil_layer)
  veil_draw.rectangle([0, 0, img.width, img.height], fill=(0, 0, 0, 120))
  img.paste(veil_layer, (0, 0), veil_layer)

  # ---------------------------------------------
  # Central ignition glow
  # ---------------------------------------------
  glow_radii = [120, 80, 40]
  for r in glow_radii:
    glow_layer = img.copy().convert("RGBA")
    glow_draw = ImageDraw.Draw(glow_layer)
    jitter = r * 0.0  # was 0.06 but I don't like it
    glow_draw.ellipse(
      [ center_x - r + rng.uniform(-jitter, jitter),
        center_y - r + rng.uniform(-jitter, jitter),
        center_x + r + rng.uniform(-jitter, jitter),
        center_y + r + rng.uniform(-jitter, jitter) ],
      fill=(120, 100, 255, 140 - r//2)
    )
    img.paste(glow_layer, (0, 0), glow_layer)

  # ---------------------------------------------
  # Lightning arcs
  # ---------------------------------------------
  arc_count = 12
  for i in range(arc_count):
    angle = (2 * math.pi / arc_count) * i
    steps = 14
    points = []
    for step in range(steps):
      t = step / (steps - 1)
      distance = inner_radius * t
      jitter_angle = angle + rng.uniform(-0.12, 0.12)
      jitter_radius = distance + rng.uniform(-10, 10)
      x = center_x + math.cos(jitter_angle) * jitter_radius
      y = center_y + math.sin(jitter_angle) * jitter_radius
      if (x - center_x) ** 2 + (y - center_y) ** 2 < outer_radius ** 2:
        points.append((x, y))
    if len(points) > 1:
      if USE_ENHANCED_LIGHTNING:
        # ----- outer electric glow -----
        draw.line(points, fill=(90,140,255,90), width=5)
        # ----- core arc -----
        draw.line(points, fill=(80,120,255,200), width=3)
        # ----- bright plasma center -----
        draw.line(points, fill=(240,250,255), width=1)
      else:
        draw.line(points, fill=(80,120,255), width=3)
        draw.line(points, fill=(220,240,255), width=1)

  # ---------------------------------------------
  # Shock outer ring
  # ---------------------------------------------
  ring_layer = img.copy().convert("RGBA")
  ring_draw = ImageDraw.Draw(ring_layer)
  ring_draw.ellipse(
    [ center_x - outer_radius,
      center_y - outer_radius,
      center_x + outer_radius,
      center_y + outer_radius],
    outline=(90, 0, 20, 200), width=2) # dark red
  img.paste(ring_layer, (0, 0), ring_layer)

  # ---------------------------------------------
  # Shock inner ring
  # ---------------------------------------------
  ring_layer = img.copy().convert("RGBA")
  ring_draw = ImageDraw.Draw(ring_layer)
  ring_draw.ellipse(
    [ center_x - inner_radius,
      center_y - inner_radius,
      center_x + inner_radius,
      center_y + inner_radius ],
    outline=(255, 40, 40, 180), width=2) # light red
  img.paste(ring_layer, (0, 0), ring_layer)

  # ---------------------------------------------
  # Hyperspace streaks
  # ---------------------------------------------
  streak_count = 24
  min_length = outer_radius + 20
  max_length = outer_radius + 80
  gap_size = 6
  for i in range(streak_count):
    angle = (2 * math.pi / streak_count) * i
    start_r = outer_radius + 4
    # ----- compute where the ray exits the image -----
    dx = math.cos(angle)
    dy = math.sin(angle)
    limit = max_length
    if dx > 0:
      limit = min(limit, (img.width - center_x) / dx)
    elif dx < 0:
      limit = min(limit, (0 - center_x) / dx)

    if dy > 0:
      limit = min(limit, (img.height - center_y) / dy)
    elif dy < 0:
      limit = min(limit, (0 - center_y) / dy)

    end_r = min(max_length, limit)
    total_length = end_r - start_r
    total_length = max(0, end_r - start_r)
    # ----- Determine if line is "long" -----
    if total_length > (max_length - min_length) * 0.6:
      gap_count = rng.choice([1, 2])
      segments = gap_count + 1
      seg_length = (total_length - gap_size * gap_count) / segments
      for s in range(segments):
        seg_start = start_r + s * (seg_length + gap_size)
        seg_end = seg_start + seg_length
        x1 = center_x + math.cos(angle) * seg_start
        y1 = center_y + math.sin(angle) * seg_start
        x2 = center_x + math.cos(angle) * seg_end
        y2 = center_y + math.sin(angle) * seg_end
        if USE_ENHANCED_HYPERSPACE:
          # ----- outer glow -----
          draw.line([(x1, y1), (x2, y2)], fill=(120,160,255,70), width=5)
          # ----- mid glow -----
          draw.line([(x1, y1), (x2, y2)], fill=(150,190,255,120), width=3)
          # ----- core streak -----
          draw.line([(x1, y1), (x2, y2)], fill=(220,240,255), width=1)
        else:
          draw.line([(x1, y1), (x2, y2)], fill=(180, 200, 255), width=2)
    else:
      x1 = center_x + math.cos(angle) * start_r
      y1 = center_y + math.sin(angle) * start_r
      x2 = center_x + math.cos(angle) * end_r
      y2 = center_y + math.sin(angle) * end_r
      if USE_ENHANCED_HYPERSPACE:
        # ----- outer glow -----
        draw.line([(x1, y1), (x2, y2)], fill=(120,160,255,70), width=5)
        # ----- mid glow -----
        draw.line([(x1, y1), (x2, y2)], fill=(150,190,255,120), width=3)
        # ----- core streak -----
        draw.line([(x1, y1), (x2, y2)], fill=(220,240,255), width=1)
      else:
        draw.line([(x1, y1), (x2, y2)], fill=(180, 200, 255), width=2)

  # ---------------------------------------------
  # Payload delivery
  # ---------------------------------------------
  padding = 6
  _, _, _, font_path_used = load_label_font()

  # ----- Decide whether we can scale -----
  if font_path_used != "PIL default":
    # ----- start with a test size -----
    test_size = 100
    font = ImageFont.truetype(font_path_used, test_size)
    # ----- find the widest line -----
    longest = max(lines, key=lambda s: font.getbbox(s)[2])
    bbox = font.getbbox(longest)
    test_width = bbox[2] - bbox[0]
    target_width = (inner_radius * 2) - padding
    final_font_size = int(test_size * target_width / test_width)
    font = ImageFont.truetype(font_path_used, final_font_size)
  else:
    # ----- fallback if only PIL default is available -----
    font = ImageFont.load_default()

  line_widths = []
  line_heights = []
  line_spacing = int(getattr(font, "size", 10) * 0.5)

  for line in lines:
    bbox = font.getbbox(line)
    line_widths.append(bbox[2] - bbox[0])
    line_heights.append(bbox[3] - bbox[1])

  text_block_height = sum(line_heights) + line_spacing * (len(lines) - 1)
  current_y = center_y - text_block_height // 2
  for i, line in enumerate(lines):
    text_x = center_x - line_widths[i] // 2

    # ----- energy glow layer -----
    text_layer = img.copy().convert("RGBA")
    text_draw = ImageDraw.Draw(text_layer)
    if FUZZY_TEXT:
      # ----- outer soft glow -----
      for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        text_draw.text((text_x+dx, current_y+dy), line, fill=(255,40,40,80), font=font)
      # ----- inner glow -----
      for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        text_draw.text((text_x+dx, current_y+dy), line, fill=(255,40,40,140), font=font)
      # ----- main text -----
      text_draw.text((text_x, current_y), line, fill=(255,40,40,220), font=font)
    else:
      # ----- bold main text only -----
      for dx, dy in [(0,0),(1,0),(0,1),(1,1)]:
        text_draw.text((text_x+dx, current_y+dy), line, fill=(255,40,40,180), font=font)

    img.paste(text_layer, (0,0), text_layer)
    current_y += line_heights[i] + line_spacing

  return img.convert("RGB"), None

# ==================================================
# CONVERT BITMAP DATA TO PIXEL GRID
# ==================================================

def build_bitmap(columns):
  """
  Convert ProffieOS column bitfields into a 2D pixel bitmap.

  Each column is a vertical bitfield where:
    - Bit 0 (LSB) represents the first pixel row.
    - Higher bits represent pixels above it.

  Returns:
    A 2D list (rows × columns) of 0/1 pixel values.
  """

  if not columns:
    return []

  height = max(max(col.bit_length(), 1) for col in columns)
  bitmap = []
  for y in range(height):
    row = []
    for col in columns:
      row.append((col >> y) & 1)
    bitmap.append(row)

  return bitmap

# ==================================================
# TRANSFORMATIONS
# ==================================================

def apply_flips(bitmap):
  """
  Apply optional horizontal and/or vertical flips
  to a bitmap according to global settings.

  Returns:
    Transformed bitmap.
  """
  if FLIP_LEFT_RIGHT:
    bitmap = [row[::-1] for row in bitmap]
  if FLIP_TOP_BOTTOM:
    bitmap = bitmap[::-1]
  return bitmap

def apply_rotation(bitmap):
  """
  Rotate bitmap according to ROTATION setting.

  Accepted values:
    0, 90, -90, 180, 270

  Returns:
    Rotated bitmap.

  Raises:
    ValueError if ROTATION is invalid.
  """
  if ROTATION == 0:
    return bitmap
  if ROTATION == 90:
    return [list(row) for row in zip(*bitmap[::-1])]
  if ROTATION in (-90, 270):
    return [list(row) for row in zip(*bitmap)][::-1]
  if ROTATION == 180:
    return [row[::-1] for row in bitmap[::-1]]
  raise ValueError("\n  Invalid ROTATION value, must be 0, 90, -90, 180, or 270")

# ==================================================
# MAIN RENDERING ENGINE / DRAWING LOOP / 4 PHASES
# ==================================================

# ==================================================
# GLYPH WIDTH HELPER
# ==================================================

def get_glyph_visual_width(glyph):
  """
  Returns the visual width used for DRAWING (not advance).

  Rules:
    - TABLE mode:
        bitmap width → glyphdata width → fallback
    - TEXT mode:
        STRICT → glyphdata width → bitmap → fallback
        NON-STRICT → WIDTH_MODE with fallback handling
  """

  bitmap = glyph["bitmap"]
  bitmap_width = len(bitmap[0]) if bitmap else 0

  advance_width = glyph["advance_width"]
  has_bitmap = bitmap_width > 0
  has_glyphdata = advance_width is not None and not glyph["status_flags"]["missing_glyphdata"]

  # ----------------------------------------
  # TABLE MODE
  # ----------------------------------------
  if RENDER_MODE == "table":
    if has_bitmap:
      return bitmap_width
    if has_glyphdata:
      return advance_width
    return FALLBACK_GLYPH_WIDTH

  # ----------------------------------------
  # TEXT MODE — STRICT
  # ----------------------------------------
  if STRICT_PROFFIE_LAYOUT:
    if has_glyphdata:
      return advance_width
    if has_bitmap:
      return bitmap_width
    return FALLBACK_GLYPH_WIDTH

  # ----------------------------------------
  # TEXT MODE — NON STRICT
  # ----------------------------------------
  if WIDTH_MODE == "glyphdata":
    if has_glyphdata:
      return advance_width
    if has_bitmap:
      return bitmap_width
    return FALLBACK_GLYPH_WIDTH

  elif WIDTH_MODE == "bitmap":
    if has_bitmap:
      return bitmap_width
    if has_glyphdata:
      return advance_width
    return FALLBACK_GLYPH_WIDTH

  elif WIDTH_MODE == "max":
    if has_bitmap and has_glyphdata:
      return max(bitmap_width, advance_width)
    if has_bitmap:
      return bitmap_width
    if has_glyphdata:
      return advance_width
    return FALLBACK_GLYPH_WIDTH

  return FALLBACK_GLYPH_WIDTH

# ==================================================
# GLYPH ADVANCE HELPER
# ==================================================

def get_glyph_advance(glyph):
  """
  Returns the horizontal cursor advance.

  TABLE:
    bitmap → glyphdata → fallback + EXTRA_GLYPH_SPACING
    (no overlap ever)

  TEXT STRICT:
    use glyphdata advance width + x_offset
    fallback to bitmap/FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING if missing

  TEXT NON-STRICT:
    WIDTH_MODE with FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING
  """

  bitmap = glyph["bitmap"]
  bitmap_width = len(bitmap[0]) if bitmap else 0

  advance_width = glyph["advance_width"]
  x_offset = glyph["x_offset"]

  has_bitmap = bitmap_width > 0
  has_glyphdata = advance_width is not None and not glyph["status_flags"]["missing_glyphdata"]

  # ----------------------------------------
  # TABLE MODE
  # ----------------------------------------
  if RENDER_MODE == "table":
    if has_bitmap:
      return bitmap_width + EXTRA_GLYPH_SPACING
    if has_glyphdata:
      return advance_width + EXTRA_GLYPH_SPACING
    return FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING

  # ----------------------------------------
  # TEXT MODE — STRICT
  # ----------------------------------------
  if STRICT_PROFFIE_LAYOUT:
    if has_glyphdata:
      return advance_width + x_offset
    if has_bitmap:
      return bitmap_width + EXTRA_GLYPH_SPACING
    return FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING

  # ----------------------------------------
  # TEXT MODE — NON STRICT
  # ----------------------------------------
  if WIDTH_MODE == "glyphdata":
    if has_glyphdata:
      return advance_width + x_offset + EXTRA_GLYPH_SPACING
    if has_bitmap:
      return bitmap_width + EXTRA_GLYPH_SPACING
    return FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING

  elif WIDTH_MODE == "bitmap":
    if has_bitmap:
      return bitmap_width + EXTRA_GLYPH_SPACING
    if has_glyphdata:
      return advance_width + x_offset + EXTRA_GLYPH_SPACING
    return FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING

  elif WIDTH_MODE == "max":
    if has_bitmap and has_glyphdata:
      return max(bitmap_width, advance_width + x_offset) + EXTRA_GLYPH_SPACING
    if has_bitmap:
      return bitmap_width + EXTRA_GLYPH_SPACING
    if has_glyphdata:
      return advance_width + x_offset + EXTRA_GLYPH_SPACING
    return FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING

  return FALLBACK_GLYPH_WIDTH + EXTRA_GLYPH_SPACING

# ==================================================
# GLYPH DRAW OFFSET
# ==================================================

def get_glyph_draw_offset(glyph):
  """
  Returns horizontal draw offset relative to cursor.

  Only used in TEXT mode when:
    - STRICT_PROFFIE_LAYOUT = True
    OR
    - WIDTH_MODE == "glyphdata"

  In TABLE mode, always 0.
  """

  if RENDER_MODE == "table":
    return 0

  if STRICT_PROFFIE_LAYOUT or WIDTH_MODE == "glyphdata":
    return glyph["x_offset"]

  return 0

# ===============================
# PHASE 1 — PREPROCESS
# ===============================

def preprocess_glyphs(glyph_records):
  """
  Phase 1: Convert raw glyph column data into transformed bitmaps.

  - Convert raw glyph data into bitmaps
  - Apply flips
  - Apply rotation

  Returns:
    List of processed glyph dictionaries ready for layout.
  """

  USE_DRAW_PAIRS = True # if false, revert to old drawing logic without build_draw_pairs()

  processed = []

  # --------------------------------------------------
  # Build and transform each glyph
  # --------------------------------------------------
  for glyph in glyph_records:

    ascii_code = glyph["ascii_code"]

    # --------------------------------------------------
    # Build unified version iterator
    # --------------------------------------------------
    if USE_DRAW_PAIRS:
      version_iter = (
        (index, pair["bitmap"], pair["glyphdata"], pair["duplicate"], pair["commented"])
        for index, pair in enumerate(glyph["draw_pairs"])
      )
    else:
      bitmap_versions = glyph["bitmap_versions"]
      glyphdata_versions = glyph["glyphdata_versions"]
      version_count = max(1, len(bitmap_versions), len(glyphdata_versions))
      active_bitmap_versions = [v for v in bitmap_versions if not v["is_commented"]]
      version_iter = (
        (
          index,
          bitmap_versions[index] if index < len(bitmap_versions) else None,
          glyphdata_versions[index] if index < len(glyphdata_versions) else None,
          index > 0,
          (
            bitmap_versions[index]["is_commented"]
            if index < len(bitmap_versions) and bitmap_versions[index]
            else False
          )
        )
        for index in range(version_count)
      )

    # --------------------------------------------------
    # Single processing loop
    # --------------------------------------------------
    for index, bitmap_version, glyphdata_version, is_duplicate, is_commented in version_iter:

      # ----------------------------------------
      # TEXT MODE → only keep primary glyph
      # ----------------------------------------
      if RENDER_MODE == "text" and index > 0:
        continue

      if bitmap_version:
        body = bitmap_version["body"]
        columns_raw = re.findall(r"0b([01]+)UL", body)
        columns = [int(col, 2) for col in columns_raw]
      else:
        columns = []

      bitmap = build_bitmap(columns)
      bitmap = apply_flips(bitmap)
      bitmap = apply_rotation(bitmap)

      if glyphdata_version:
        y_offset = glyphdata_version["y_offset"]
        x_offset = glyphdata_version["x_offset"]
        advance_width = glyphdata_version["advance_width"]
      elif glyph["primary_glyphdata"]:
        # ----- fallback to primary glyphdata selected by parser -----
        y_offset = glyph["primary_glyphdata"]["y_offset"]
        x_offset = glyph["primary_glyphdata"]["x_offset"]
        advance_width = glyph["primary_glyphdata"]["advance_width"]
      else:
        y_offset = 0
        x_offset = 0
        advance_width = None

      processed.append({
        "bitmap": bitmap,
        "y_offset": y_offset,
        "x_offset": x_offset,
        "advance_width": advance_width,
        "ascii_code": ascii_code,
        "is_first_duplicate": (index == 0),
        "is_commented": (bitmap_version and bitmap_version["is_commented"]),
        "status_flags": glyph["status_flags"]
      })

  return processed

# ===============================
# PHASE 2 — BUILD LINES
# ===============================

def build_lines(processed):
  """
  Phase 2: Build glyph stream and resolve line wrapping.

  Unified layout engine for BOTH table and text modes.

  Handles:
    - Explicit newlines characters (\n) in text mode
    - AUTO_WRAP behavior
    - Width-based wrapping
    - Table wrapping (always wraps)
    - Clipping when AUTO_WRAP is False

  Returns:
    List of lines, where each line is a list of glyph dicts.
  """

  # ----------------------------------------
  # TEXT MODE → build glyph stream from text
  # ----------------------------------------
  if RENDER_MODE == "text":
    glyph_stream = []
    for ch in CUSTOM_TEXT:
      ascii_code = ord(ch)
      if ch == "\n":
        glyph_stream.append({
          "ascii_code": 10,
          "bitmap": [],
          "y_offset": 0,
          "width": 0,
          "status_flags": {
            "missing_bitmap": True,
            "missing_glyphdata": True
          }
        })
        continue
      glyph = next( (candidate_glyph for candidate_glyph in processed if candidate_glyph["ascii_code"] == ascii_code), None )
      if glyph:
        glyph_stream.append(glyph)

  else:
    # ----- TABLE MODE → just use all glyphs -----
    glyph_stream = processed

  # ----------------------------------------
  # WRAPPING ENGINE
  # ----------------------------------------
  lines = []
  current_line = []
  current_width = 0

  global DISPLAY_WIDTH
  if DISPLAY_WIDTH < 32:
    DISPLAY_WIDTH = 32
    report_geometry_correction()

  for glyph in glyph_stream:

    # ----------------------------------------
    # Explicit newline handling (TEXT MODE ONLY)
    # ----------------------------------------
    if RENDER_MODE == "text" and glyph["ascii_code"] == 10:
      lines.append(current_line)
      current_line = []
      current_width = 0
      continue

    glyph_advance = get_glyph_advance(glyph)

    # ----------------------------------------
    # Decide wrapping behavior
    # ----------------------------------------
    should_wrap = False

    if RENDER_MODE == "table":
      # ----- Always wrap in table mode -----
      if current_line and current_width + glyph_advance > DISPLAY_WIDTH:
        should_wrap = True

    elif RENDER_MODE == "text":
      if AUTO_WRAP:
        wrap_advance = glyph_advance if glyph_advance > 0 else 0
        if current_line and current_width + wrap_advance > DISPLAY_WIDTH:
          should_wrap = True
      else:
        # ----- No wrapping → clipping allowed -----
        should_wrap = False

    # ----------------------------------------
    # Apply wrap
    # ----------------------------------------
    if should_wrap:
      lines.append(current_line)
      current_line = []
      current_width = 0

    current_line.append(glyph)
    current_width += glyph_advance

  if current_line:
    lines.append(current_line)

  return lines

# ===============================
# PHASE 3 — LAYOUT COMPUTATION
# ===============================

def compute_layout(lines, spacing, add_spacing_after_last):
  """
  Phase 3: Compute ascent, descent, height, width and baseline positions for each line.

  Returns:
    rendered_lines (list of dict)
    total_height (int)
    baseline_positions (list)
    cap_positions (list)
    descent_positions (list)
  """

  # --------------------------------------------------
  # Determine ascent & descent per line
  # --------------------------------------------------
  rendered_lines = []
  total_height = 0

  baseline_positions = []
  cap_positions = []
  descent_positions = []

  for i, line in enumerate(lines):
    ascent = 0
    descent = 0
    line_width = 0
    line_glyphs = []

    for glyph in line:
      # --------------------------------------------------
      # Determine advance according to mode
      # --------------------------------------------------
      advance = get_glyph_advance(glyph)

      # --------------------------------------------------
      # Skip bitmap metrics if missing, but still draw
      # --------------------------------------------------
      bitmap = glyph["bitmap"]
      height = len(bitmap) if bitmap else 0
      y_offset = glyph["y_offset"] if USE_Y_OFFSET else 0

      ascent = max(ascent, -y_offset)
      descent = max(descent, height + y_offset)

      line_width += advance
      line_glyphs.append(glyph)

    line_height = ascent + descent
    rendered_lines.append({
      "glyphs": line_glyphs,
      "ascent": ascent,
      "descent": descent,
      "height": line_height,
      "width": line_width
    })

    total_height += line_height

    # --------------------------------------------------
    # Add spacing between lines
    # --------------------------------------------------
    if i < len(lines) - 1 or add_spacing_after_last:
      total_height += spacing

    # --------------------------------------------------
    # Baseline / cap / descent positions for this line
    # --------------------------------------------------
    baseline_positions.append(total_height - descent)
    cap_positions.append(total_height - line_height)
    descent_positions.append(total_height - 1)

  # --------------------------------------------------
  # Enforce minimum/maximum height
  # --------------------------------------------------
  if DISPLAY_HEIGHT_HARD_LIMIT and (RENDER_MODE == "text" or RENDER_MODE == "random"):
    total_height = DISPLAY_HEIGHT
  else:
    total_height = max(total_height, DISPLAY_HEIGHT)
  return (
    rendered_lines,
    total_height,
    baseline_positions,
    cap_positions,
    descent_positions
  )

# ===============================
# PHASE 4 — DRAWING ENGINE
# ===============================

def render_glyphs(glyph_records, average_width):
  """
  Main font rendering engine.
  Render full font in table or text mode.

  Pipeline / Phases:
  1. Pre-process glyphs
  2. Build lines (with dynamic spacing for labels)
  3. Compute layout metrics
  4. Draw glyph pixels

     Collect label anchor positions
     Delegate frame/legend/diagnostics to add_borders_and_scale()

  Returns:
    Final rendered image.
  """

  # ------------------------------
  # PHASE 1 — PREPROCESS
  # ------------------------------
  processed = preprocess_glyphs(glyph_records)

  glyph_draw_index = {}
  glyph_total_count = {}

  for glyph in processed:
    ascii_code = glyph["ascii_code"]

    if ascii_code not in glyph_total_count:
      glyph_total_count[ascii_code] = 0

    glyph_total_count[ascii_code] += 1

  any_duplicates = any(
    glyph["status_flags"]["duplicate_bitmap"] or
    glyph["status_flags"]["duplicate_glyphdata"]
    for glyph in processed
  )

  # ------------------------------
  # PHASE 2 — LINE BUILDING
  # ------------------------------
  lines = build_lines(processed)

  # ------------------------------
  # PHASE 3 — LAYOUT COMPUTATION
  # ------------------------------
  # ------------------------------
  # Load label font early (needed for spacing logic)
  # ------------------------------
  label_font = None
  font_height = 0

  if SHOW_LABEL and RENDER_MODE == "table":
    label_font, font_height, _, _ = load_label_font()

    required_scaled = font_height + 8 + 16 # 8 + 16 for label padding
    required_unscaled = (required_scaled + SCALE - 1) // SCALE
    effective_spacing = max(SPACING, required_unscaled)
  else:
    effective_spacing = SPACING

  add_spacing_after_last = SHOW_LABEL and RENDER_MODE == "table"

  (
    rendered_lines,
    total_height,
    baseline_positions,
    cap_positions,
    descent_positions
  ) = compute_layout(
    lines,
    effective_spacing,
    add_spacing_after_last
  )

  # ------------------------------
  # PHASE 4 — DRAWING ENGINE
  # ------------------------------
  global DISPLAY_WIDTH
  if DISPLAY_WIDTH < 32:
    DISPLAY_WIDTH = 32
    report_geometry_correction()

  global WHITE, GREY, RED, ORANGE, YELLOW, BLACK, PURPLE

  global LABEL_START
  if LABEL_START not in (0, 1):
    LABEL_START = 1

  if BLACK_AND_WHITE_ONLY:
    if INVERT_BLACK_AND_WHITE:
      canvas_color = 255
      mono_pixel = 0
    else:
      canvas_color = 0
      mono_pixel = 255

    img = Image.new(BLACK_AND_WHITE_MODE, (DISPLAY_WIDTH, total_height), canvas_color)

    # ----- translate every logical color into monochrome -----
    WHITE  = mono_pixel
    GREY   = mono_pixel
    RED    = mono_pixel
    YELLOW = mono_pixel
    ORANGE = mono_pixel
    BLACK  = mono_pixel
    PURPLE = mono_pixel

  else:
    img = Image.new("RGB", (DISPLAY_WIDTH, total_height), BLACK)

  label_entries = []
  y_cursor = 0

  for i, line in enumerate(rendered_lines):

    if ROW_ALIGN == "left":
      x_cursor = 0
    elif ROW_ALIGN == "center":
      x_cursor = (DISPLAY_WIDTH - line["width"]) // 2
    elif ROW_ALIGN == "right":
      x_cursor = DISPLAY_WIDTH - line["width"]
    else:
      raise ValueError("Invalid ROW_ALIGN")

    baseline = y_cursor + line["ascent"]
    baseline_positions.append(baseline)
    cap_positions.append(y_cursor)
    descent_positions.append(y_cursor + line["height"] - 1)

    for index, glyph in enumerate(line["glyphs"]):
      bitmap = glyph["bitmap"]
      y_offset = glyph["y_offset"] if USE_Y_OFFSET else 0
      glyph_width = get_glyph_visual_width(glyph)
      bitmap_width = len(bitmap[0]) if bitmap else 0
      glyph_height = len(bitmap) if bitmap else 1

      # --------------------------------------------------
      # COMPLETELY MISSING CHAR → RED BLOCK
      # --------------------------------------------------
      if (
        glyph["status_flags"]["missing_bitmap"] and
        glyph["status_flags"]["missing_glyphdata"] and
        DRAW_MISSING_BLOCK
      ):

        line_top = baseline - line["ascent"]
        for yy in range(line_top, baseline + 1):
          for xx in range(glyph_width):
            img.putpixel((x_cursor + xx, yy), RED)

      # --------------------------------------------------
      # YELLOW → bitmap exists but no GLYPHDATA
      # --------------------------------------------------
      elif glyph["status_flags"]["missing_glyphdata"]:
        if bitmap:
          for y in range(glyph_height):
            for x in range(bitmap_width):
              if bitmap[y][x]:
                target_y = baseline - (glyph_height - 1 - y)
                img.putpixel((x_cursor + x, target_y), YELLOW)

      # --------------------------------------------------
      # ORANGE → empty bitmap
      # --------------------------------------------------
      elif not bitmap:
        glyph_width = (
          glyph["advance_width"]
          if glyph["advance_width"] is not None
          else FALLBACK_GLYPH_WIDTH
        )

        line_top = baseline - line["ascent"]
        start_y = baseline + y_offset

        if start_y > baseline:
          start_y = baseline

        if start_y < line_top:
          start_y = line_top

        if RENDER_MODE == "text":
          pixel_color = BLACK
        else:
          pixel_color = ORANGE

        for yy in range(line_top, start_y + 1):
          for xx in range(glyph_width):
            img.putpixel((x_cursor + xx, yy), pixel_color)

      # --------------------------------------------------
      # GREY → commented bitmap
      # --------------------------------------------------
      elif glyph.get("is_commented", False):
        if SHOW_COMMENTED:
          for y in range(glyph_height):
            for x in range(bitmap_width):
              if bitmap[y][x]:
                target_y = baseline + y_offset + y
                img.putpixel((x_cursor + x, target_y), GREY)

      # --------------------------------------------------
      # DUPLICATE DEFINITIONS → FIRST WHITE, OTHERS GREY
      # --------------------------------------------------
      elif (
        glyph["status_flags"]["duplicate_bitmap"] or
        glyph["status_flags"]["duplicate_glyphdata"]
      ):

        if bitmap:
          pixel_color = (
            WHITE if glyph.get("is_first_duplicate", False)
            else GREY
          )

          for y in range(glyph_height):
            for x in range(bitmap_width):
              if bitmap[y][x]:
                target_y = baseline + y_offset + y
                img.putpixel((x_cursor + x, target_y), pixel_color)

      # --------------------------------------------------
      # NORMAL GLYPH DRAWING → WHITE or ORANGE if the GLYPHDATA geometry has a problem
      # --------------------------------------------------
      else:
        if bitmap:
          for y in range(glyph_height):
            for x in range(bitmap_width):
              if bitmap[y][x]:
                target_y = baseline + y_offset + y
                px = x_cursor + x
                img.putpixel((px, target_y), WHITE)

      # --------------------------------------------------
      # GLYPH LABELS DRAWING
      # --------------------------------------------------
      if SHOW_LABEL and RENDER_MODE == "table" and not BLACK_AND_WHITE_ONLY:

        # ----- Determine label color (match glyph logic except for active duplicates) -----
        if glyph.get("is_commented", False):
          label_color = GREY
        elif glyph["status_flags"]["duplicate_bitmap"] or glyph["status_flags"]["duplicate_glyphdata"]:
          label_color = RED
        elif glyph["status_flags"]["missing_bitmap"] and glyph["status_flags"]["missing_glyphdata"]:
          label_color = RED
        elif glyph["status_flags"]["missing_glyphdata"]:
          label_color = YELLOW
        elif (not glyph["bitmap"]):
          label_color = ORANGE
        else:
          label_color = WHITE

        glyph_center = x_cursor + glyph_width // 2
        descent_line = y_cursor + line["height"] - 1

        ascii_code = glyph["ascii_code"]

        if ascii_code == 32:
          base_char = "sp"
        elif ascii_code is not None:
          base_char = chr(ascii_code)
        else:
          base_char = "?"

        total = glyph_total_count.get(ascii_code, 1)
        if LABEL_NUMBERING and total > 1:
          # ----- initialize draw index -----
          if ascii_code not in glyph_draw_index:

            if LABEL_INCREMENT:
              glyph_draw_index[ascii_code] = LABEL_START - 1
            else: # LABEL "DECREMENT"
              # ----- start one step ABOVE the first value so first decrement lands correctly -----
              glyph_draw_index[ascii_code] = total + LABEL_START

          # ----- update index depending on mode -----
          if LABEL_INCREMENT:
            glyph_draw_index[ascii_code] += 1
          else:
            glyph_draw_index[ascii_code] -= 1

          current_index = glyph_draw_index[ascii_code]
          # ----- final label -----
          label_char = f"{base_char}-{current_index}"
        else:
          label_char = base_char

        label_entries.append({
          "char": chr(glyph["ascii_code"]) if glyph["ascii_code"] is not None else "?",
          "label":label_char,
          "center_x_unscaled": glyph_center,
          "descent_y_unscaled": descent_line,
          "color": label_color
        })

      # ----------------------------------------
      # Show advance position
      # ----------------------------------------
      if SHOW_GLYPH_ORIGIN: # and RENDER_MODE == "table":
        for yy in range(y_cursor, y_cursor + line["height"]):
          if 0 <= x_cursor < DISPLAY_WIDTH:
            img.putpixel((x_cursor, yy), PURPLE)

      # ----------------------------------------
      # Advance cursor
      # ----------------------------------------
      advance = get_glyph_advance(glyph)
      x_cursor += advance

    y_cursor += line["height"]
    if i < len(rendered_lines) - 1:
      y_cursor += effective_spacing

  if BLACK_AND_WHITE_ONLY:
    img, _ = inner_core_critical_hit(img)
    return img
  else:
    return add_borders_and_scale(
      img,
      baseline_positions,
      cap_positions,
      descent_positions,
      label_entries,
      any_duplicates
    )

# ==================================================
# RENDER SINGLE BITMAP ARRAY (RENDER_MODE == "random" or "this")
# ==================================================

def render_single_bitmap(filename, output_name):
  """
  Render a single bitmap array from a .h file.

  Used when RENDER_MODE == "random" or "this"

  Responsibilities:
    - Locate a specific bitmap array by name (LOOK_FOR)
    - Extract column bitfields (for display only, forgiving missing 0b/UL)
    - Build bitmap grid
    - Render as an image
    - Optionally apply borders and scaling
    - Generate a minimal analysis text file

  Returns:
    PIL.Image object (scaled and bordered if DO_BORDERS is True),
    or None if the bitmap array is not found.

  Notes:
    - This mode bypasses font-wide parsing.
    - Intended for testing individual bitmap arrays.
  """

  if RENDER_MODE == "random":
    with open(filename, "r", encoding="utf-8") as f:
      content = f.read()

    pattern = rf"const\s+uint\d+_t\s+{LOOK_FOR}\[\]\s*=\s*\{{(.*?)\}};"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
      print(f"\n  {LOOK_FOR} not found, exiting script.")
      print("")
      print("                                           MTFBWY")
      return None

    body = match.group(1)
    source_name = LOOK_FOR

  else: # RENDER_MODE == "this"
    body = THIS
    source_name = '"THIS"'

  lines = [l.strip() for l in body.splitlines() if l.strip()]

  # ----- Validate comma placement -----
  if len(lines) > 1:
    for line in lines[:-1]:
      if not line.endswith(","):
        print(f"\n  Error: {source_name} does not contain valid bitmap columns separated by a comma.")
        print(f"\n  ProffieOS expected format: 0bXXXXXXXXUL,")
        print(f"\n  GLYPHY accepts messy formats like: '0bXXXXXXXX,' or 'XXXXXXXXUL,' or 'XXXXXXXX,'.")
        print(f"\n  You are probably looking at a pretty arrangement of zeros and ones.")
        print(f"\n  No valid messy binary columns separated by commas were found.")
        print("")
        print(f"          Please insert coins or commas to try again!")
        print(f"          ===========================================")
        print("")
        print(f"                                               MTFBWY\n")
        return None, None

  # ----- Forgiving parser for 0b...UL columns -----
  missing_0b_count = 0
  missing_ul_count = 0
  raw_columns = []

  for token in body.split(","):
    token = token.strip()
    if not token:
      continue

    # ----- Handle missing 0b -----
    if token.startswith("0b"):
      bin_str = token[2:]
    else:
      bin_str = token
      missing_0b_count += 1

    # ----- Handle missing UL -----
    if bin_str.endswith("UL"):
      bin_str = bin_str[:-2]
    else:
      missing_ul_count += 1

    # ----- Keep only 0 and 1 digits -----
    bin_str = "".join(c for c in bin_str if c in "01")
    if not bin_str:
      continue

    raw_columns.append(int(bin_str, 2))

  # ----- Convert to columns for bitmap rendering -----
  bitmap = build_bitmap(raw_columns)

  height = len(bitmap)
  width = len(bitmap[0]) if bitmap else 0

  # ----- Ensure display geometry -----
  global DISPLAY_WIDTH, DISPLAY_HEIGHT, SCALE

  if DISPLAY_WIDTH < 32:
    DISPLAY_WIDTH = 32
    report_geometry_correction()
  if DISPLAY_HEIGHT < 32:
    DISPLAY_HEIGHT = 32
    report_geometry_correction()
  if SCALE < 1:
    SCALE = 1
    report_geometry_correction()

  # ----- Create image -----
  if BLACK_AND_WHITE_ONLY:
    if INVERT_BLACK_AND_WHITE:
      canvas_color = 255
      drawing_color = 0
    else:
      canvas_color = 0
      drawing_color = 255
    img = Image.new(BLACK_AND_WHITE_MODE, (width, height), canvas_color)
  else:
    img = Image.new("RGB", (width, height), BLACK)
    drawing_color = WHITE

  # ----- Draw pixels -----
  for y in range(height):
    for x in range(width):
      if bitmap[y][x]:
        img.putpixel((x, y), drawing_color)

  # ----- Crop to display -----
  if DISPLAY_HEIGHT:
    img = img.crop((0, 0, DISPLAY_WIDTH, min(height, DISPLAY_HEIGHT)))
  else:
    img = img.crop((0, 0, DISPLAY_WIDTH, height))

  # ----- Analysis file -----
  if GENERATE_REPORT:
    base = os.path.splitext(output_name)[0]
    analysis_file = os.path.join(OUTPUT_DIR, f"{base}_Analysis.txt")
    with open(analysis_file, "w", encoding="utf-8") as f:
      f.write("\n")
      f.write(f"Bitmap source: {source_name}, size: width {width} x height {height}\n")
      if missing_0b_count or missing_ul_count:
        f.write("\n")
        f.write(f"  WARNING: {source_name} has {missing_0b_count} missing '0b' and {missing_ul_count} missing 'UL' entries.\n")
        f.write("\n")
        f.write(f"    ProffieOS will probably not accept it but GLYPHY will. 😉\n")
      if width > DISPLAY_WIDTH:
        f.write("\n")
        f.write(f"  WARNING: Bitmap width {width}px exceeds DISPLAY_WIDTH {DISPLAY_WIDTH}px.\n")
      if DISPLAY_HEIGHT and height > DISPLAY_HEIGHT:
        f.write("\n")
        f.write(f"  WARNING: Bitmap height {height}px exceeds DISPLAY_HEIGHT {DISPLAY_HEIGHT}px.\n")
      f.write("\n")
      f.write(f"                                           MTFBWY")

  # ----- Print to screen -----
  print("")
  print(f"  Bitmap source: {source_name}, size: width {width} x height {height}")
  if missing_0b_count or missing_ul_count:
    print("")
    print(f"  Warning: {source_name} has {missing_0b_count} missing '0b' and {missing_ul_count} missing 'UL' entries")
    print("")
    print("    ProffieOS will probably not accept it but GLYPHY will.")
  if width > DISPLAY_WIDTH:
    print("")
    print(f"  Warning: Bitmap width {width}px exceeds DISPLAY_WIDTH {DISPLAY_WIDTH}px.")
  if DISPLAY_HEIGHT and height > DISPLAY_HEIGHT:
    print("")
    print(f"  Warning: Bitmap height {height}px exceeds DISPLAY_HEIGHT {DISPLAY_HEIGHT}px.")
  print("")
  print(f"                                           MTFBWY")
  if GENERATE_REPORT:
    print("")
    print(f"  Saved report: /{OUTPUT_DIR}/{analysis_file}")

  # ----- Return image with optional scaling and borders -----
  if BLACK_AND_WHITE_ONLY:
    img, _ = inner_core_critical_hit(img)
    return img, analysis_file
  else:
    if DO_BORDERS:
      return add_borders_and_scale(img, [], [], [], [], False), analysis_file
    else:
      scaled = img.resize((img.width * SCALE, img.height * SCALE), Image.NEAREST)
      scaled, _ = inner_core_critical_hit(scaled)
      return scaled, analysis_file

# ==================================================
# APPLY DIAGNOSTIC TICKS OVERLAYS (before scaling)
# ==================================================

def apply_diagnostics_overlay_ticks(
  bordered,
  baseline_positions,
  cap_positions,
  descent_positions
):
  """
  Draw diagnostic tick markers (before scaling).

  Includes:
    - Top interval ticks
    - Left interval ticks
    - Baseline marker
    - Cap-height & descent markers
  """

  if ( not DISPLAY_DIAGNOSTIC or INNER_BLACK_BORDER < 1):
    return bordered

  BORDERS = OUTER_WHITE_BORDER + INNER_BLACK_BORDER

  # --------------------------------------------------
  # Draw vertical position markers in Top border (White)
  # --------------------------------------------------
  if VERTICAL_GRID_MARKERS and INNER_BLACK_BORDER > 0 and VERTICAL_GRID_INTERVAL > 1:
    right_inner = bordered.width - BORDERS
    x = BORDERS
    while x < right_inner:
      bordered.putpixel((x, OUTER_WHITE_BORDER), WHITE)
      x += VERTICAL_GRID_INTERVAL

  # --------------------------------------------------
  # Draw end of vertical position markers in Top Left border (Red)
  # --------------------------------------------------
  if VERTICAL_EDGE_MARKER and INNER_BLACK_BORDER > 0:
    top_right_x = bordered.width - BORDERS
    bordered.putpixel((top_right_x, OUTER_WHITE_BORDER), RED)

  # --------------------------------------------------
  # Draw horizontal position markers in Left border (White)
  # --------------------------------------------------
  if HORIZONTAL_GRID_MARKERS and INNER_BLACK_BORDER > 0 and HORIZONTAL_GRID_INTERVAL > 1:
    end_y = bordered.height - BORDERS
    marker_x = OUTER_WHITE_BORDER  # leftmost pixel inside black border
    y = BORDERS
    while y < end_y:
      bordered.putpixel((marker_x, y), WHITE)
      y += HORIZONTAL_GRID_INTERVAL

  # --------------------------------------------------
  # Draw horizontal Cap-height (Light Blue) and Descent markers in Right border (Green)
  # --------------------------------------------------

  #SHIFT_CAP_DESC_LEFT       = True   # To shift the right blue & green tick marks 1 left ← disabled and made automatic
                                      # (to avoid being overwritten by the red tick marks when they overlap).
  if DRAW_CAP_DESC_MARKERS and INNER_BLACK_BORDER > 0:
    right_x = bordered.width - OUTER_WHITE_BORDER - 1
    #if INNER_BLACK_BORDER >= 2 and SHIFT_CAP_DESC_LEFT:   # SHIFT_CAP_DESC_LEFT disabled and made automatic
    if INNER_BLACK_BORDER >= 2:
      blue_x = right_x - 1
    else:
      blue_x = right_x
    if cap_positions:
      for y in cap_positions:
        draw_y = y + BORDERS
        if draw_y < bordered.height - OUTER_WHITE_BORDER:
          bordered.putpixel((blue_x, draw_y), BLUE)
    if descent_positions:
      for y in descent_positions:
        draw_y = y + BORDERS
        if draw_y < bordered.height - OUTER_WHITE_BORDER:
          bordered.putpixel((blue_x, draw_y), GREEN)

  # --------------------------------------------------
  # Draw horizontal Baseline markers in Right border (Red)
  # --------------------------------------------------
  if DRAW_BASELINE_MARKER and INNER_BLACK_BORDER > 0 and baseline_positions:
    right_x = bordered.width - OUTER_WHITE_BORDER - 1
    for baseline in baseline_positions:
      y = baseline + BORDERS
      if y < bordered.height - OUTER_WHITE_BORDER:
        bordered.putpixel((right_x, y), RED)

  return bordered

# ==================================================
# APPLY DIAGNOSTIC LINES OVERLAYS (after scaling)
# ==================================================

def apply_diagnostics_overlay_lines(
  bordered,
  baseline_positions,
  cap_positions,
  descent_positions,
  font_frame_scaled_bottom
):
  """
  Draw diagnostic grid and guide lines (after scaling).

  Includes:
    - Vertical grid lines (grey)
    - Horizontal grid lines (grey)
    - Baseline lines (red)
    - Cap-height (blue) & descent (green) lines
    - Vertical right edge line (red)

  Priority:
    RED > BLUE/GREEN > GREY > BLACK
    Glyph pixels (WHITE/YELLOW/ORANGE/RED block) are never overwritten.
  """

  if not DISPLAY_DIAGNOSTIC:
    return bordered

  # --------------------------------------------------
  # Unscaled border offset (used for computing glyph Y positions)
  # --------------------------------------------------
  BORDERS = OUTER_WHITE_BORDER + INNER_BLACK_BORDER

  # --------------------------------------------------
  # Scaled limits for drawing inside text area
  # --------------------------------------------------
  scaled_borders = BORDERS * SCALE

  right_limit  = bordered.width - scaled_borders
  bottom_limit = font_frame_scaled_bottom - scaled_borders

  # --------------------------------------------------
  # Overwrite rules
  # --------------------------------------------------
  def can_draw(current, new_color):

    if current in (RED, YELLOW, ORANGE, WHITE):
      return False

    if new_color == RED:
      return True

    if new_color in (BLUE, GREEN):
      return current in (BLACK, GREY)

    if new_color == GREY:
      return current == BLACK

    return False

  # --------------------------------------------------
  # Vertical Grey Grid Lines (VERTICAL_GRID_INTERVAL)
  # --------------------------------------------------
  if VERTICAL_GRID_LINES and VERTICAL_GRID_INTERVAL > 1:

    x = scaled_borders + VERTICAL_GRID_INTERVAL * SCALE
    while x < right_limit:
      for y in range(scaled_borders, bottom_limit):
        current = bordered.getpixel((x, y))
        if can_draw(current, GREY):
          bordered.putpixel((x, y), GREY)
      x += VERTICAL_GRID_INTERVAL * SCALE

  # --------------------------------------------------
  # Vertical Red Right Edge Line
  # --------------------------------------------------
  if VERTICAL_EDGE_LINE and INNER_BLACK_BORDER > 0:
    x_scaled = bordered.width - scaled_borders
    for y in range(scaled_borders, bottom_limit):
      current = bordered.getpixel((x_scaled, y))
      if can_draw(current, RED):
        bordered.putpixel((x_scaled, y), RED)

  # --------------------------------------------------
  # Horizontal Grey Grid Lines (HORIZONTAL_GRID_INTERVAL)
  # --------------------------------------------------
  if HORIZONTAL_GRID_LINES and HORIZONTAL_GRID_INTERVAL > 1:
    logical_y = BORDERS + HORIZONTAL_GRID_INTERVAL
    logical_end = (font_frame_scaled_bottom // SCALE) - BORDERS
    while logical_y < logical_end:
      scaled_y = logical_y * SCALE + (SCALE - 1)
      if 0 <= scaled_y < bordered.height:
        for x in range(scaled_borders, right_limit):
          current = bordered.getpixel((x, scaled_y))
          if can_draw(current, GREY):
            bordered.putpixel((x, scaled_y), GREY)
      logical_y += HORIZONTAL_GRID_INTERVAL

  # --------------------------------------------------
  # Horizontal Blue Cap-height – TOP of scaled row
  # --------------------------------------------------
  if SHOW_HORIZ_CAP_DESC_LINES:
    for y in cap_positions:
      scaled_y = (y + BORDERS) * SCALE
      if 0 <= scaled_y < bordered.height:
        for x in range(scaled_borders, right_limit):
          current = bordered.getpixel((x, scaled_y))
          if can_draw(current, BLUE):
            bordered.putpixel((x, scaled_y), BLUE)

    # --------------------------------------------------
    # Horizontal Green Descent – BOTTOM of scaled row
    # --------------------------------------------------
    for y in descent_positions:
      scaled_y = (y + BORDERS) * SCALE + (SCALE - 1)
      if 0 <= scaled_y < bordered.height:
        for x in range(scaled_borders, right_limit):
          current = bordered.getpixel((x, scaled_y))
          if can_draw(current, GREEN):
            bordered.putpixel((x, scaled_y), GREEN)

  # --------------------------------------------------
  # Horizontal Red Baseline – BOTTOM of scaled row
  # --------------------------------------------------
  if SHOW_HORIZ_BASE_LINES:
    for y in baseline_positions:
      scaled_y = (y + BORDERS) * SCALE + (SCALE - 1)
      if 0 <= scaled_y < bordered.height:
        for x in range(scaled_borders, right_limit):
          current = bordered.getpixel((x, scaled_y))
          if can_draw(current, RED):
            bordered.putpixel((x, scaled_y), RED)

  return bordered

# ==================================================
# BORDER CONSTRUCTION
# ==================================================

def add_borders_and_scale(
  img,
  baseline_positions,
  cap_positions,
  descent_positions,
  label_entries,
  any_duplicates
):
  """
  Construct final image frame.

  Steps:
  1. Add outer/inner borders
  2. Draw diagnostic tick markers (pre-scale)
  3. Optionally append legend area
  4. Scale image
  5. Draw diagnostic grid/guide lines (post-scale)
  6. Draw legend contents
  7. Draw glyph labels inside spacing region

  Returns:
    Final rendered image.
  """

  font = None
  if (SHOW_LEGEND and DISPLAY_DIAGNOSTIC) or (SHOW_LABEL and RENDER_MODE == "table"):
    font, font_height, font_size, font_path_used = load_label_font()

  if ( (SHOW_LEGEND and DISPLAY_DIAGNOSTIC) or not (RENDER_MODE == "random" or RENDER_MODE == "this") ):
    labels_left  = ["BASELINE", "ASCEND", "DESCEND", "GRID"]
    title_left   =  "DIAGNOSTIC LEGEND"
    labels_right = ["MISSING", "NO BITMAP", "NO DATA", "NORMAL", "COMMENTED / DUPES"]
    title_right  =  "GLYPH LEGEND"
    special_right_label = "COMMENTED / DUPES" # it is special because it can partially change color
    special_right_label1 = "COMMENTED / "
    special_right_label2 = "DUPES"

    # ==================================================
    # MEASURE LEFT BLOCK / COLUMNS 1 to 3
    # ==================================================
    def measure_left_block(font, labels_left, title_left):

      TITLE_SPACING = 6
      VERTICAL_SPACING = 6
      TICK_SIZE = 5
      COLUMN_GAP = 12

      if DISPLAY_WIDTH < 64:
        LINE_LENGTH = 15 * SCALE
      else:
        LINE_LENGTH = 20 * SCALE

      # ----- Title -----
      bbox = font.getbbox(title_left)
      title_width  = bbox[2] - bbox[0]
      title_height = bbox[3] - bbox[1]

      # ----- Tallest row label -----
      max_label_height = max(
        font.getbbox(label)[3] - font.getbbox(label)[1]
        for label in labels_left
      )

      row_height = max_label_height + VERTICAL_SPACING

      total_height = (
        title_height +
        TITLE_SPACING +
        VERTICAL_SPACING +
        (len(labels_left) * row_height)
      )

      # ----- Width -----
      max_label_width = max(
        font.getbbox(label)[2] for label in labels_left
      )

      width = (
        TICK_SIZE +
        COLUMN_GAP +
        LINE_LENGTH +
        COLUMN_GAP +
        max_label_width
      )

      return {
        "width": width,
        "height": total_height,
        "title_width": title_width,
        "title_height": title_height,
        "row_height": row_height,
        "rows": len(labels_left),
        "tick_size": TICK_SIZE,
        "column_gap": COLUMN_GAP,
        "line_length": LINE_LENGTH,
        "title_spacing": TITLE_SPACING
      }

    # ==================================================
    # MEASURE RIGHT BLOCK / COLUMN 5 & 6
    # ==================================================
    def measure_right_block(font, labels_right, title_right):

      TITLE_SPACING = 6
      VERTICAL_SPACING = 6
      COLUMN_GAP = 12
      BOX_HEIGHT = 3 * SCALE
      BOX_WIDTH  = 6 * SCALE

      # ----- Title -----
      bbox = font.getbbox(title_right)
      title_width  = bbox[2] - bbox[0]
      title_height = bbox[3] - bbox[1]

      # ----- Tallest row element -----
      max_label_height = max(
        font.getbbox(label)[3] - font.getbbox(label)[1]
        for label in labels_right
      )

      max_row_element = max(max_label_height, BOX_HEIGHT)

      row_height = max_row_element + VERTICAL_SPACING

      total_height = (
        title_height +
        TITLE_SPACING +
        VERTICAL_SPACING +
        (len(labels_right) * row_height)
      )

      # ----- Width -----
      max_label_width = max(
        font.getbbox(label)[2] for label in labels_right
      )

      width = (
        BOX_WIDTH +
        COLUMN_GAP +
        max_label_width
      )

      return {
        "width": width,
        "height": total_height,
        "title_width": title_width,
        "title_height": title_height,
        "row_height": row_height,
        "rows": len(labels_right),
        "box_width": BOX_WIDTH,
        "box_height": BOX_HEIGHT,
        "column_gap": COLUMN_GAP,
        "title_spacing": TITLE_SPACING
      }

    # ==================================================
    # LAYOUT LEGEND BLOCKS / COLUMN 1, 2, 3, 5 & 6
    # ==================================================
    def layout_legend_blocks(
      left,
      right,
      show_left,
      show_right,
      inner_left,
      inner_top,
      inner_width,
      inner_height
    ):

      half_width = inner_width // 2
      center_x = inner_left + half_width

      # ----- Only ONE block visible -----
      if show_left and not show_right:

        top = inner_top + (inner_height - left["height"]) // 2
        left_start_x = inner_left + (inner_width - left["width"]) // 2

        return {
          "left_start_x": left_start_x,
          "right_start_x": None,
          "top_left": top,
          "top_right": None,
          "center_x": None
        }

      if show_right and not show_left:

        top = inner_top + (inner_height - right["height"]) // 2
        right_start_x = inner_left + (inner_width - right["width"]) // 2

        return {
          "left_start_x": None,
          "right_start_x": right_start_x,
          "top_left": None,
          "top_right": top,
          "center_x": None
        }

      # ----- BOTH blocks visible -----
      tallest_height = max(left["height"], right["height"])

      tallest_block_top = (
        inner_top +
        (inner_height - tallest_height) // 2
      )

      # ----- Determine which is taller -----
      left_is_taller = left["height"] >= right["height"]

      # ----- Horizontal centering inside halves -----
      left_start_x = inner_left + (
        (half_width - left["width"]) // 2
      )

      right_start_x = center_x + (
        (half_width - right["width"]) // 2
      )

      # ----- Vertical placement -----
      if left_is_taller:
        top_left = tallest_block_top
        top_right = tallest_block_top
      else:
        top_left = tallest_block_top
        top_right = tallest_block_top

      return {
        "left_start_x": left_start_x,
        "right_start_x": right_start_x,
        "top_left": top_left,
        "top_right": top_right,
        "center_x": center_x
      }

  # --------------------------------------------------
  # Create bordered image  (before scaling)
  # --------------------------------------------------
  global OUTER_WHITE_BORDER, INNER_BLACK_BORDER, SCALE

  if OUTER_WHITE_BORDER < 0:
    OUTER_WHITE_BORDER = 0
    report_geometry_correction()

  if INNER_BLACK_BORDER < 0:
    INNER_BLACK_BORDER = 0
    report_geometry_correction()

  if SCALE < 1:
    SCALE = 1
    report_geometry_correction()

  BORDERS = OUTER_WHITE_BORDER + INNER_BLACK_BORDER

  # --------------------------------------------------
  # If no borders → skip border drawing entirely
  # --------------------------------------------------
  if BORDERS <= 0:
    bordered = img.copy()
  else:
    bordered = Image.new("RGB", ( img.width + 2 * BORDERS, img.height + 2 * BORDERS ), WHITE)

  # ----- Paste original image inside borders -----
  bordered.paste(img, (BORDERS, BORDERS))

  # ----- Draw inner black frame ONLY if INNER_BLACK_BORDER > 0 -----
  if INNER_BLACK_BORDER > 0:

    for x in range(OUTER_WHITE_BORDER, bordered.width - OUTER_WHITE_BORDER):
      for y in range(OUTER_WHITE_BORDER, BORDERS):
        bordered.putpixel((x, y), BLACK)
      for y in range(
        bordered.height - BORDERS,
        bordered.height - OUTER_WHITE_BORDER
      ):
        bordered.putpixel((x, y), BLACK)

    for y in range(OUTER_WHITE_BORDER, bordered.height - OUTER_WHITE_BORDER):
      for x in range(OUTER_WHITE_BORDER, BORDERS):
        bordered.putpixel((x, y), BLACK)
      for x in range(
        bordered.width - BORDERS,
        bordered.width - OUTER_WHITE_BORDER
      ):
        bordered.putpixel((x, y), BLACK)

  # ==================================================
  # DIAGNOSTIC OVERLAY TICKS (before scaling)
  # ==================================================
  bordered = apply_diagnostics_overlay_ticks(
    bordered,
    baseline_positions,
    cap_positions,
    descent_positions
  )

  bordered, _ = inner_core_critical_hit(bordered)

  # ==================================================
  # DRAW LEGEND AREA (before scaling)
  # ==================================================
  if SHOW_LEGEND and DISPLAY_DIAGNOSTIC and not ( RENDER_MODE == "random" or RENDER_MODE == "this" ):

    # --------------------------------------------------
    # Idiot-proof Dynamic legend height (never too small)
    # --------------------------------------------------

    left = measure_left_block( font, labels_left, title_left )
    right = measure_right_block( font, labels_right, title_right )

    diagnostic_visible = (
      DRAW_BASELINE_MARKER or
      DRAW_CAP_DESC_MARKERS or
      SHOW_HORIZ_BASE_LINES or
      SHOW_HORIZ_CAP_DESC_LINES
    )

    show_left = diagnostic_visible
    show_right = True

    if ENABLE_DEVELOPER_DEBUG_MODE:
      """
      # Keep this for diagnostic when changing columns geometry, commented to avoid unnecessary visual pollution.
      print("debug LEFT BLOCK measured height:", left["height"])
      print("debug RIGHT BLOCK measured height:", right["height"])
      """

    # ----- Determine tallest block in SCALED space -----
    if show_left and show_right:
      tallest_unscaled = max(left["height"], right["height"])
    elif show_left:
      tallest_unscaled = left["height"]
    else:
      tallest_unscaled = right["height"]

    LEGEND_TARGET_VERTICAL_VISUAL_PADDING = 8 # this one will go in my GLOBALS

    extra_padding_scaled = max(0, LEGEND_TARGET_VERTICAL_VISUAL_PADDING - INNER_BLACK_BORDER * SCALE)

    # ----- Convert to unscaled height -----
    # Divide by SCALE and ROUND UP (ceil)
    legend_vertical_padding = ((extra_padding_scaled + SCALE - 1) // SCALE)
    legend_height_unscaled = ( (tallest_unscaled + SCALE - 1) // SCALE )

    primary_block = "left" if diagnostic_visible else "right"

    new_height = bordered.height + legend_height_unscaled + BORDERS + legend_vertical_padding * 2 # 2 for top & bottom

    if ENABLE_DEVELOPER_DEBUG_MODE:
      """
      # Keep this for diagnostic when changing columns geometry, commented to avoid unnecessary visual pollution.
      print("debug LEGEND AREA INNER HEIGHT:", legend_height_unscaled, " (before scaling)")
      print("debug LEGEND AREA INNER HEIGHT:", legend_height_unscaled * SCALE, " = ",
        legend_height_unscaled, " * ",SCALE , " computed (what is should be after scaling)")
      """

    legend_img = Image.new("RGB", (bordered.width, new_height), BLACK)
    legend_img.paste(bordered, (0, 0))

    # ----- Bottom outer white border -----
    for x in range(legend_img.width):
      for y in range(new_height - OUTER_WHITE_BORDER, new_height):
        legend_img.putpixel((x, y), WHITE)

    # ----- Left & Right outer white borders -----
    for y in range(bordered.height, new_height):
      for x in range(OUTER_WHITE_BORDER):
        legend_img.putpixel((x, y), WHITE)
      for x in range(legend_img.width - OUTER_WHITE_BORDER, legend_img.width):
        legend_img.putpixel((x, y), WHITE)

    inner_top = bordered.height + INNER_BLACK_BORDER
    inner_bottom = new_height - BORDERS
    inner_height = inner_bottom - inner_top
    glyph_frame_height_before_legend = bordered.height
    bordered = legend_img

  # --------------------------------------------------
  # SCALE IMAGE
  # --------------------------------------------------
  scaled = bordered.resize(
    (bordered.width * SCALE, bordered.height * SCALE),
    Image.NEAREST
  )

  draw = ImageDraw.Draw(scaled)

  # --------------------------------------------------
  # Compute true bottom of font frame
  # --------------------------------------------------
  if SHOW_LEGEND and DISPLAY_DIAGNOSTIC and not  ( RENDER_MODE == "random" or RENDER_MODE == "this" ):
    font_frame_scaled_bottom = glyph_frame_height_before_legend * SCALE
  else:
    font_frame_scaled_bottom = bordered.height * SCALE

  # ==================================================
  # DIAGNOSTIC OVERLAY LINES (after scaling)
  # ==================================================
  scaled = apply_diagnostics_overlay_lines(
    scaled,
    baseline_positions,
    cap_positions,
    descent_positions,
    font_frame_scaled_bottom
  )

  # ==================================================
  # DRAW LEGEND DETAILS (after scaling)
  # ==================================================
  if SHOW_LEGEND and DISPLAY_DIAGNOSTIC and not ( RENDER_MODE == "random" or RENDER_MODE == "this" ):

    # ----------------------------------------
    # Scaled geometry
    # ----------------------------------------
    outer_scaled_border = OUTER_WHITE_BORDER * SCALE
    inner_scaled_border = INNER_BLACK_BORDER * SCALE
    inner_left   = outer_scaled_border
    inner_right  = scaled.width - outer_scaled_border
    inner_top    = font_frame_scaled_bottom + inner_scaled_border
    inner_bottom = scaled.height - outer_scaled_border - inner_scaled_border
    inner_width  = inner_right - inner_left
    inner_height = inner_bottom - inner_top

    # ----------------------------------------
    # Measure blocks
    # ----------------------------------------
    left = measure_left_block(font,labels_left,title_left)
    right = measure_right_block(font,labels_right,title_right)

    # --------------------------------------------------
    # Determine PRIMARY block width requirement
    # --------------------------------------------------
    if primary_block == "left":
      primary_width = left["width"]
    else:
      primary_width = right["width"]

    # ----- Minimum scale needed for legend to fit -----
    usable_width_unscaled = bordered.width - 2 * (OUTER_WHITE_BORDER + INNER_BLACK_BORDER)

    if usable_width_unscaled <= 0:
      min_scale = SCALE
    else:
      min_scale = (
        (primary_width + usable_width_unscaled - 1)
        // usable_width_unscaled
      )

    # --------------------------------------------------
    # BACKUP BLOCK (legend area too small to fit legend data)
    # --------------------------------------------------
    #if ENABLE_DEVELOPER_DEBUG_MODE: # Uncomment here, and comment next line to "force see" BACKUP block.
    if primary_width > inner_width:

      words = ["Increase", "SCALING", f"to {min_scale}", "to see", "legend"]
      LINE_SPACING = 6

      # ----- Measure total height -----
      total_height = 0
      line_metrics = []

      for w in words:
        bbox = font.getbbox(w)
        text_h = bbox[3] - bbox[1]
        line_metrics.append((w, text_h))
        total_height += text_h

      total_height += LINE_SPACING * (len(words) - 1)

      # ----- Vertical center -----
      start_y = inner_top + (inner_height - total_height) // 2
      y = start_y

      for word, text_h in line_metrics:
        bbox = font.getbbox(word)
        text_w = bbox[2] - bbox[0]

        # ----- Horizontal center (even if inside borders) -----
        x = inner_left + (inner_width - text_w) // 2

        # ----- Horizontal clamp -----
        if x < inner_left:
          x = inner_left

        draw.text((x, y), word, fill=WHITE, font=font)
        y += text_h + LINE_SPACING

      return scaled

    # ----------------------------------------
    # Layout
    # ----------------------------------------
    layout = layout_legend_blocks(
      left,
      right,
      show_left,
      show_right,
      inner_left,
      inner_top,
      inner_width,
      inner_height
    )

    tick_colors = [RED, BLUE, GREEN, WHITE]
    line_colors = [RED, BLUE, GREEN, GREY]
    box_colors  = [RED, ORANGE, YELLOW, WHITE, GREY]

    # ==================================================
    # DRAW LEFT BLOCK / COLUMNS 1 to 3
    # ==================================================
    if show_left:

      left_start_x = layout["left_start_x"]
      top_left     = layout["top_left"]

      # ----- Title -----
      title_x = left_start_x + (left["width"] - left["title_width"]) // 2
      draw.text((title_x, top_left), title_left, fill=WHITE, font=font)

      rows_top = (
        top_left +
        left["title_height"] +
        left["title_spacing"]
      )

      for i, label in enumerate(labels_left):
        row_top    = rows_top + i * left["row_height"]
        row_center = row_top + left["row_height"] // 2
        x_tick = left_start_x
        x_line = x_tick + left["tick_size"] + left["column_gap"]
        x_text = x_line + left["line_length"] + left["column_gap"]

        # ----- Tick (5x5) -----
        tick_top = row_center - left["tick_size"] // 2
        for yy in range(left["tick_size"]):
          for xx in range(left["tick_size"]):
            px = x_tick + xx
            py = tick_top + yy
            if 0 <= px < scaled.width and 0 <= py < scaled.height:
              scaled.putpixel((px, py), tick_colors[i])

        # ----- Line -----
        for dx in range(left["line_length"]):
          px = x_line + dx
          if 0 <= px < scaled.width and 0 <= row_center < scaled.height:
            scaled.putpixel((px, row_center), line_colors[i])

        # ----- Label -----
        bbox = font.getbbox(label)
        text_height = bbox[3] - bbox[1]
        text_y = row_center - text_height // 2
        draw.text((x_text, text_y), label, fill=WHITE, font=font)

    # ==================================================
    # DRAW CENTER LINE IF NEEDED / COLUMN 4
    # ==================================================
    if layout["center_x"] is not None:
      for y in range(inner_top, inner_bottom):
        if 0 <= layout["center_x"] < scaled.width:
          scaled.putpixel((layout["center_x"], y), GREY)

    # ==================================================
    # DRAW RIGHT BLOCK / COLUMN 5 & 6
    # ==================================================
    if show_right and layout["right_start_x"] is not None:
      right_start_x = layout["right_start_x"]
      top_right     = layout["top_right"]

      # ----- Title -----
      title_x = right_start_x + (right["width"] - right["title_width"]) // 2
      draw.text((title_x, top_right), title_right, fill=WHITE, font=font)

      rows_top = (
        top_right +
        right["title_height"] +
        right["title_spacing"]
      )

      for i, (label, color) in enumerate(zip(labels_right, box_colors)):
        row_top    = rows_top + i * right["row_height"]
        row_center = row_top + right["row_height"] // 2
        x_box  = right_start_x
        x_text = x_box + right["box_width"] + right["column_gap"]

        # ----- Rectangle -----
        box_top = row_center - right["box_height"] // 2
        for yy in range(right["box_height"]):
          for xx in range(right["box_width"]):
            px = x_box + xx
            py = box_top + yy
            if 0 <= px < scaled.width and 0 <= py < scaled.height:
              scaled.putpixel((px, py), color)

        # ----- DUP text inside grey box -----
        if label == special_right_label:
          bbox_dup = font.getbbox("DUP")
          dup_w = bbox_dup[2] - bbox_dup[0]
          dup_h = bbox_dup[3] - bbox_dup[1]
          dup_x = x_box + (right["box_width"] - dup_w) // 2
          dup_y = row_center - dup_h // 2 - bbox_dup[1]
          draw.text((dup_x, dup_y), "DUP", fill=RED, font=font)

        # ----- Label -----
        bbox = font.getbbox(label)
        text_height = bbox[3] - bbox[1]
        text_y = row_center - text_height // 2
        if label == special_right_label:

          # ----- Draw left part (always white) -----
          draw.text((x_text, text_y), special_right_label1, fill=WHITE, font=font)
          left_bbox = font.getbbox(special_right_label1)
          left_width = left_bbox[2] - left_bbox[0]

          # ----- Draw right part (red or white) -----
          dup_color = RED if any_duplicates else WHITE
          draw.text(
            (x_text + left_width, text_y),
            special_right_label2,
            fill=dup_color,
            font=font
          )

        else:
          draw.text((x_text, text_y), label, fill=WHITE, font=font)

  # ==================================================
  # DRAW GLYPH LABELS (inside spacing region)
  # ==================================================
  if SHOW_LABEL and RENDER_MODE == "table":

    scaled_borders = BORDERS * SCALE

    for entry in label_entries:

      center_x_scaled = entry["center_x_unscaled"] * SCALE + scaled_borders
      descent_scaled = entry["descent_y_unscaled"] * SCALE + scaled_borders
      label_text = entry.get("label", entry["char"])
      bbox = font.getbbox(label_text)
      text_width = bbox[2] - bbox[0]
      text_height = bbox[3] - bbox[1]
      label_x = center_x_scaled - text_width // 2

      # ----- Draw inside spacing area -----
      label_y = descent_scaled + 8
      if 0 <= label_y < scaled.height:
        draw.text(
          (label_x, label_y),
          label_text,
          fill=entry["color"],
          font=font
        )

  # ==================================================
  # Developer TTF debug
  # ==================================================
  if ENABLE_DEVELOPER_DEBUG_MODE and SHOW_LEGEND and DISPLAY_DIAGNOSTIC and not  ( RENDER_MODE == "random" or RENDER_MODE == "this" ):
    if not SHOW_LABEL:
      font, font_height, font_size, font_path_used = load_label_font()

    TTF_DISTANCE = 4

    # ----------------------------------------
    # Determine side
    # ----------------------------------------
    if show_left and show_right:
      draw_side = "left" if left["height"] < right["height"] else "right"
    elif show_left:
      draw_side = "left"
    else:
      draw_side = "left"

    # ----------------------------------------
    # Build debug string
    # ----------------------------------------
    if draw_side == "left":
      ttf_debug = (
        f"TTF: {font_path_used}, "
        f"height:{font_height}px, "
        f"size:{font_size}"
      )
    else:
      ttf_debug = (
        f"size:{font_size}, "
        f"height:{font_height}px, "
        f"TTF: {font_path_used}"
      )

    # ----------------------------------------
    # Measure text
    # ----------------------------------------
    bbox = font.getbbox(ttf_debug)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # ----------------------------------------
    # Width rule
    # ----------------------------------------
    if show_left and show_right:
      max_width = scaled.width // 2 - TTF_DISTANCE - OUTER_WHITE_BORDER * SCALE
    else:
      max_width = scaled.width - TTF_DISTANCE * 2 - OUTER_WHITE_BORDER  * SCALE * 2

    # ----------------------------------------
    # Clip if needed
    # ----------------------------------------
    if text_w > max_width:
      if draw_side == "left":
        clipped = ttf_debug
        while clipped:
          clipped = clipped[:-1]
          bbox = font.getbbox(clipped + "…")
          if (bbox[2] - bbox[0]) <= max_width:
            ttf_debug = clipped + "…"
            break
      else:
        clipped = ttf_debug
        while clipped:
          clipped = clipped[1:]
          bbox = font.getbbox("…" + clipped)
          if (bbox[2] - bbox[0]) <= max_width:
            ttf_debug = "…" + clipped
            break

      bbox = font.getbbox(ttf_debug)
      text_w = bbox[2] - bbox[0]
      text_h = bbox[3] - bbox[1]

    # ----------------------------------------
    # Vertical limit
    # ----------------------------------------
    top = scaled.height - OUTER_WHITE_BORDER * SCALE - TTF_DISTANCE - text_h

    # ----------------------------------------
    # Final placement
    # ----------------------------------------
    if draw_side == "left":
      x = OUTER_WHITE_BORDER * SCALE + TTF_DISTANCE
    else:
      x = scaled.width - OUTER_WHITE_BORDER * SCALE - TTF_DISTANCE - text_w

    y = top

    draw.text(
      (x, y),
      ttf_debug,
      fill=WHITE,
      font=font
    )

  return scaled

# ==================================================
# AUTO OPEN Windows / macOS / Linux
# ==================================================

def open_file(path):
  """Open a file using the default application, cross-platform."""

  system = platform.system()
  # ----- Windows -----
  if system == "Windows":
    os.startfile(path)
  # ----- macOS -----
  elif system == "Darwin":
    subprocess.run(["open", path])
  # ----- Linux / Unix (xdg-open) -----
  else:
    subprocess.run(["xdg-open", path])

# ==================================================
# FILENAME OUTPUT GENERATION
# ==================================================

def generate_output_name(base_name):
  """
  Generate output filename based on FILENAME_MODE.

  Modes:
    - overwrite
    - iterate (adds numeric suffix)

  Returns:
    Filename string.
  """

  ext = "bmp" if BLACK_AND_WHITE_ONLY else OUTPUT_FORMAT

  if FILENAME_MODE == "overwrite":
    return f"{base_name}.{ext}"

  if FILENAME_MODE == "iterate":

    max_range = 99 if FILENAME_ITERATE_RANGE is None else max(1, int(FILENAME_ITERATE_RANGE))
    digits = len(str(max_range))
    used_numbers = set()

    # --------------------------------------------------
    # Try from 1 up to max_range
    # --------------------------------------------------
    prefix = base_name + "_"
    prefix_len = len(prefix)

    for file in os.listdir(OUTPUT_DIR):
      if not file.startswith(prefix):
        continue
      name_part = file[prefix_len:]
      number_str = name_part.split("_")[0].split(".")[0]
      if number_str.isdigit():
        used_numbers.add(int(number_str))

    for i in range(1, max_range + 1):
      if i not in used_numbers:
        return f"{base_name}_{i:0{digits}d}.{ext}"

    # --------------------------------------------------
    # If full → overwrite zero version
    # --------------------------------------------------
    return f"{base_name}_{0:0{digits}d}.{ext}"

  raise ValueError("Invalid FILENAME_MODE, please select iterate or overwrite.")

# ==================================================
# REPORT OUTPUT GENERATION
# ==================================================

def write_report_file(
  output_name,
  font_file,
  ctx,
  font_path,
  font_size,
  font_height
):
  """
  Write full validation report to file.
  Only summary is printed to console.
  """

  metrics = ctx["metrics"]
  diagnostics = ctx["diagnostics"]
  severity = ctx["severity_totals"]
  report_details = ctx["report_details"]

  average_bitmap_width = metrics["average_bitmap_width"]
  average_bitmap_height = metrics["average_bitmap_height"]
  average_advance_width = metrics["average_advance_width"]
  average_x_offset = metrics["average_x_offset"]
  average_y_offset = metrics["average_y_offset"]
  max_height_char = metrics["max_height_char"]
  max_height = metrics["max_height"]
  max_descent_char = metrics["max_descent_char"]
  max_descent = metrics["max_descent"]
  widest_bitmap_char = metrics["widest_bitmap_char"]
  widest_bitmap_width = metrics["widest_bitmap_width"]
  widest_advance_char = metrics["widest_advance_char"]
  widest_advance_width = metrics["widest_advance_width"]

  total_errors = diagnostics["total_errors"]
  total_bg_errors = diagnostics["total_bg_errors"]
  if total_bg_errors["enabled"]:
    fragments = total_bg_errors["details"]["fragments"]
  total_critical = diagnostics["total_critical_chars"]
  total_found = diagnostics["total_found"]
  total_missing_characters = diagnostics["total_missing_characters"]
  total_missing_bitmap = diagnostics["total_missing_bitmap"]
  total_missing_glyphdata = diagnostics["total_missing_glyphdata"]
  total_commented_bitmap_only = diagnostics["total_commented_bitmap_only"]
  total_commented_glyphdata_only = diagnostics["total_commented_glyphdata_only"]
  total_duplicate_bitmap = diagnostics["total_duplicate_bitmap"]
  total_duplicate_glyphdata = diagnostics["total_duplicate_glyphdata"]

  if GENERATE_REPORT:
    base = os.path.splitext(output_name)[0]
    report_name = f"{base}_Analysis.txt"
    report_path = os.path.join(OUTPUT_DIR, report_name)

    with open(report_path, "w", encoding="utf-8") as f:

      # --------------------------------------------------
      # HEADER
      # --------------------------------------------------
      f.write("=" * 62 + "\n")
      #f.write("================ GLYPHY FONT ANALYSIS REPORT: ================\n")
      f.write("=" * 16 + " GLYPHY FONT ANALYSIS REPORT: " + "=" * 16 + "\n")
      f.write("=" * 62 + "\n\n")
      f.write(f"Font name: {font_file}\n")
      f.write("Total characters expected: 95 (char0 to char94)\n")
      f.write(f"Total characters found: {total_found}\n")
      f.write(f"Total characters with Issues: {total_errors}\n")
      f.write(f"Total characters with Critical errors: {total_critical}\n")
      f.write("\n")
      # --------------------------------------------------
      # SEVERITY BREAKDOWN
      # --------------------------------------------------
      f.write("=" * 18 + " GLYPHY FONT DIAGNOSTICS: " + "=" * 17 + "\n")
      f.write(f"Totally missing characters: {total_missing_characters}\n")
      f.write(f"Missing bitmap arrays: {total_missing_bitmap}\n")
      f.write(f"Missing GLYPHDATA entries: {total_missing_glyphdata}\n")
      f.write(f"Bitmap only commented out: {total_commented_bitmap_only}\n")
      f.write(f"GLYPHDATA only commented out: {total_commented_glyphdata_only}\n")
      f.write(f"Duplicate active bitmap definitions: {total_duplicate_bitmap}\n")
      f.write(f"Duplicate active GLYPHDATA definitions: {total_duplicate_glyphdata}\n")
      f.write("\n")
      f.write("=" * 18 + " GLYPHY SEVERITY SUMMARY: " + "=" * 17 + "\n")
      f.write(f"Critical messages: {severity['critical']}\n")
      f.write(f"Error messages: {severity['error']}\n")
      f.write(f"Warning messages: {severity['warning']}\n")
      f.write(f"Info messages: {severity['info']}\n")
      f.write("\n")
      # --------------------------------------------------
      # FONT STATISTICS
      # --------------------------------------------------
      #f.write("================== GLYPHY FONT STATISTICS: ===================\n")
      f.write("=" * 18 + " GLYPHY FONT STATISTICS: " + "=" * 19 + "\n")
      f.write(f"Tallest glyph height: {max_height_char} ({max_height} px)\n")
      f.write(f"Largest descent: {max_descent_char} ({max_descent} px)\n")
      f.write(f"Widest bitmap: {widest_bitmap_char} ({widest_bitmap_width} px)\n")
      f.write(f"Widest advance_width: {widest_advance_char} ({widest_advance_width}) px\n")
      f.write(f"Average bitmap width: {average_bitmap_width} px\n")
      f.write(f"Average bitmap height: {average_bitmap_height} px\n")
      f.write(f"Average advance_width: {average_advance_width} px\n")
      f.write(f"Average x_offset: {average_x_offset} px\n")
      f.write(f"Average y_offset: {average_y_offset} px\n")
      f.write("\n")
      # --------------------------------------------------
      # DETAILED VALIDATION OUTPUT
      # --------------------------------------------------
      #f.write("==================== GLYPHY FONT DETAILS: ====================\n\n")
      f.write("=" * 20 + " GLYPHY FONT DETAILS: " + "=" * 20 + "\n\n")

      if report_details:
        for line in report_details:
          f.write(line + "\n")
      else:
        f.write("\n")
        f.write("           All 95 characters are complete and valid.           \n\n")
        f.write("\n")

      f.write("                     Thank you for using GLYPHY\n")
      f.write("                           Created by Oli\n\n")
      if total_bg_errors["enabled"]:
        indent = " " * 62
        f.write(f"{indent}MTFBWY\n\n")
        fragment_line = " ".join(f"{f:08X}" for f in fragments)
        f.write(f"{indent}{fragment_line}\n\n")
      else:
        f.write(" " * 31 +"MTFBWY\n\n")

      # --------------------------------------------------
      # DEVELOPER DEBUG SECTION
      # --------------------------------------------------
      #f.write("===================== DEVELOPER DEBUG DATA: ==================\n\n")
      f.write("=" * 20 + " DEVELOPER DEBUG DATA: " + "=" * 19 + "\n\n")
      f.write("\n")
      f.write("  Generated with GLYPHY version 56\n")
      if ENABLE_DEVELOPER_DEBUG_MODE:
        from datetime import datetime
        now = datetime.now()

        f.write("\n")
        f.write(f"  debug System date: {now.strftime('%Y - %m_%b - %d')}\n")
        f.write(f"  debug System time: {now.strftime('%H:%M:%S')}\n")

        if SHOW_LABEL or SHOW_LEGEND:
          f.write("\n")
          f.write(f"debug TTF font used: {font_path}\n")
          f.write(f"debug TTF Font size: {font_size}\n")
          f.write(f"debug TTF Font height: {font_height}px\n")

    if AUTO_OPEN_REPORT:
      open_file(report_path)

  # --------------------------------------------------
  # Print to screen
  # --------------------------------------------------
  print("\nFont analysis summary:")
  print("======================================\n")
  print(f"  Found: {total_found}/95")
  print(f"  Characters with Issues: {total_errors}")
  print(f"  Characters with Critical Errors: {total_critical}")
  print("")
  print(f"  Totally missing characters: {total_missing_characters}")
  print(f"  Missing bitmap arrays: {total_missing_bitmap}")
  print(f"  Missing GLYPHDATA entries: {total_missing_glyphdata}")
  print(f"  Bitmap only commented out: {total_commented_bitmap_only}")
  print(f"  GLYPHDATA only commented out: {total_commented_glyphdata_only}")
  print(f"  Duplicate active bitmap definitions: {total_duplicate_bitmap}")
  print(f"  Duplicate active GLYPHDATA definitions: {total_duplicate_glyphdata}")
  print("")
  print(f"  Critical Characters: {severity['critical']}")
  print(f"  Errors: {severity['error']}")
  print(f"  Warnings: {severity['warning']}")
  print(f"  Info: {severity['info']}")
  if not GENERATE_REPORT and (severity['critical'] or severity['error'] or severity['warning'] or severity['info']):
    print("")
    print("  Please set GENERATE_REPORT to True to see details.")

  if GENERATE_REPORT:
    return report_path
  else:
    return None

# ==================================================
# SKELETON OUTPUT GENERATION
# ==================================================

def create_skeleton_font(filename):
  """
  Generate fully validator-compliant ProffieOS font skeleton with:
  - const uint8_t arrays
  - ASCII comments for characters & GLYPHDATA
  - Valid 0b0UL columns
  - Proper pt7b naming
  - Placeholder GLYPHDATA references
  """

  base = os.path.splitext(os.path.basename(filename))[0]
  fallback = max(5, int(FALLBACK_GLYPH_WIDTH))

  with open(filename, "w", encoding="utf-8") as f:
    f.write(f"// GLYPHY GENERATED SKELETON {filename}               MTFBWY\n\n")
    # --------------------------------------------------
    # Bitmap arrays
    # --------------------------------------------------
    for glyph_index in range(95):
      ascii_code = glyph_index + 32
      ascii_char = chr(ascii_code)
      f.write(
        f"const uint8_t {base}pt7bChar{glyph_index}[] = {{   // 0x{ascii_code:02X} '{ascii_char}'\n"
        f"  0b0UL,\n"
        f"  0b0UL\n}};\n"
      )

    # --------------------------------------------------
    # GLYPHDATA table
    # --------------------------------------------------
    f.write(f"const Glyph {base}pt7bGlyphs[] = {{\n")
    for glyph_index in range(95):
      ascii_code = glyph_index + 32
      ascii_char = chr(ascii_code)
      if not (glyph_index == 94):
        f.write(
          f"  {{   {fallback},    0,    {fallback + 1}, "
          f"GLYPHDATA({base}pt7bChar{glyph_index}) }},   "
          f"// 0x{ascii_code:02X} '{ascii_char}'\n"
        )
      else:
        f.write(
          f"  {{   {fallback},    0,    {fallback + 1}, "
          f"GLYPHDATA({base}pt7bChar{glyph_index}) }} }}; "
          f"// 0x{ascii_code:02X} '{ascii_char}'\n"
        )
    f.write("\n")

# ==================================================
# REPAIR MENU ENTRY POINT / "FIX-FONT" MODE
# ==================================================

def run_repair_menu(font_file, ctx):
  """
  Never modify the original.
  Always append.
  Hard limit: 999 clones.
  Countdown warning starts at 900.
  """

  # --------------------------------------------------
  # SINGLE KEY INPUT Windows / macOS / Linux
  # --------------------------------------------------

  def get_single_key(valid_keys):
    """
    Read a single keypress without requiring ENTER.
    Only returns when a key in valid_keys is pressed.
    """

    system = platform.system()

    # ----- Windows -----
    if system == "Windows":
      import msvcrt
      while True:
        key = msvcrt.getch().decode("utf-8", errors="ignore")
        if key in valid_keys:
          print(key)
          return key

    # ----- macOS -----
    elif system == "Darwin":
      import tty
      import termios
      fd = sys.stdin.fileno()
      old = termios.tcgetattr(fd)
      try:
        tty.setraw(fd)
        while True:
          key = sys.stdin.read(1)
          if key in valid_keys:
            print(key)
            return key
      finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    # ----- Linux / Unix -----
    else:
      import tty
      import termios
      fd = sys.stdin.fileno()
      old = termios.tcgetattr(fd)
      try:
        tty.setraw(fd)
        while True:
          key = sys.stdin.read(1)
          if key in valid_keys:
            print(key)
            return key
      finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

  print("\n======================================")
  print("Glyphy Repair Mode")
  print("======================================\n")
  print("USE AT YOUR OWN RISK:")
  print("Experimental & not fully tested")
  print("--------------------------------------")
  print("- Glyphy will NEVER modify the original file")
  print("- Glyphy will NEVER modify the glyph art (you must do that yourself)")
  print("- Glyphy will NEVER overwrite an output file")
  print("   └──> you have up to 999 repair attempts to get it right")
  print("- Fixed .h text fonts are written to the default output folder")
  print("- Only ONE repair tool runs per execution")
  print("\n  Available repair tools:")
  print("  --------------------------------------")
  print("  1. Fix incorrect uintXX_t types")
  print("  2. Fix missing ASCII comments (missing comments will be added automatically using the suggested value)")
  print("  3. Fix missing '0b' and 'UL', please ensure you have binaries separated by comas!")
  print("  4. Fix missing glyphs (bitmap array and/or GLYPHDATA)")
  print("  5. Fix missing 'pt7b'")
  #print("  6. What else could be added here? No, I will not delete duplicates — you must do that yourself.")
  print("  0. Exit")

  print("\n  Select repair tool: ", end="", flush=True)
  choice = get_single_key({"0","1","2","3","4","5"})

  if choice == "0":
    return

  # --------------------------------------------------
  # Clone generator (hard limit 999)
  # --------------------------------------------------

  base = os.path.splitext(os.path.basename(font_file))[0]
  ext = os.path.splitext(font_file)[1]

  # ----- Normalize base name (strip existing _fixed_XXX) -----
  base_match = re.match(r"^(.*)_fixed_\d{3}$", base)
  if base_match:
    base = base_match.group(1)

  existing = set()

  # ----- Scan working + output folders for existing clones -----
  clone_re = re.compile(rf"{re.escape(base)}_fixed_(\d{{3}}){re.escape(ext)}$")

  for folder in (".", OUTPUT_DIR):
    for name in os.listdir(folder):

      if not name.startswith(base) or "_fixed_" not in name:
        continue

      clone_match = clone_re.match(name)
      if clone_match:
        existing.add(int(clone_match.group(1)))

  # ----- Find next available clone slot -----
  for clone_index in range(1, 1000):
    if clone_index not in existing:
      clone_name = f"{base}_fixed_{clone_index:03d}{ext}"
      clone_path = os.path.join(OUTPUT_DIR, clone_name)

      if ENABLE_DEVELOPER_DEBUG_MODE:
        remaining = 999 - max(existing, default=0) # use this to test the limit instead of else line ============================
      else:
        remaining = 999 - len(existing)

      if remaining < 100:
        print(f"\n  WARNING: only {remaining} clone slots remaining")
      break
  else:
    raise RuntimeError("\n  Maximum clone count reached (999).")
  print(f"\n  Working on clone: {clone_name}")

  with open(font_file, "r", encoding="utf-8") as font_handle:
    lines = font_handle.readlines()

  fixed_lines = []
  uint_fixes = 0
  missing_bitmap_comments = 0
  incorrect_bitmap_comments = 0
  missing_glyphdata_comments = 0
  incorrect_glyphdata_comments = 0
  binary_repairs = 0
  bitmap_additions = 0
  glyphdata_additions = 0
  pt7b_additions = 0

  uint_pattern = re.compile(r'uint(\d+)_t')
  bitmap_pattern = re.compile(r'Char(\d+)\[\]')
  comment_prefix = re.compile(r"^//\s*0x([0-9A-Fa-f]{2})\s*'(.{1})'")
  glyphdata_pattern = re.compile(r'GLYPHDATA\(\s*([A-Za-z0-9_]+Char(\d+))\s*\)')

  # ==================================================
  # COMMENT FIX HELPER
  # ==================================================

  def fix_glyph_comment(line, ascii_code, expected, comment_prefix,
                        missing_comments, incorrect_comments,
                        context_label):

    parts = line.split("//", 1)

    # ----- Missing comment → auto add -----
    if len(parts) == 1:
      missing_comments += 1
      line = line.rstrip() + " " + expected + "\n"
      return line, missing_comments, incorrect_comments, False

    # ----- Existing comment -----
    existing = parts[1]
    # remove leading // and spaces after them
    existing_text = existing.lstrip("/").lstrip(" ")
    # remove trailing spaces/newline
    existing_text = existing_text.rstrip()
    existing = f"// {existing_text}"

    m = comment_prefix.match(existing)
    valid = False
    if m:
      hex_code = int(m.group(1), 16)
      char = m.group(2)
      if hex_code == ascii_code and char == chr(ascii_code):
        valid = True
    if valid:
      return line, missing_comments, incorrect_comments, False

    # ----- Comment mismatch -----
    incorrect_comments += 1

    print(f"\n  {context_label} comment mismatch:")
    print("  --------------------------------------")
    print(f'  Correct: "{expected}" Current: "{existing}"')
    print(f"\n  1. Auto-fix to: {expected}")
    print(f"  2. Combine both: {expected} {existing_text}")
    print("  3. Enter custom comment")
    print("  4. Save progress and exit")
    print("\n  Choice: ", end="", flush=True)
    option = get_single_key({"1","2","3","4"})

    if option == "1":
      final = expected
    elif option == "2":
      final = f"{expected} {existing_text}"
    elif option == "3":
      user = input("Enter custom comment: ").strip()
      user = user.lstrip("/").strip()
      final = f"   // {user}"
    elif option == "4":
      print("\n  Glyphy repair interrupted by user.")
      print("  Partial fixes were saved. Exiting repair tool...")
      return line, missing_comments, incorrect_comments, True
    else:
      final = expected
    line = parts[0].rstrip() + final + "\n"
    return line, missing_comments, incorrect_comments, False

  # ==================================================
  # FIRST PASS : BITMAP ARRAYS
  # ==================================================

  for line_index, line in enumerate(lines):

    # ---------------------------------------------
    # 1. UINT FIX (uses parser ctx)
    # ---------------------------------------------
    if choice == "1":
      bitmap_match = bitmap_pattern.search(line)
      if bitmap_match:
        glyph_index = int(bitmap_match.group(1))
        versions = ctx["bitmap_dict"].get(glyph_index, [])
        for version in versions:
          declared = version.get("uint_declared")
          correct = version.get("correct_uint")
          if correct and declared != correct:
            new_uint = f"uint{correct}_t"
            line = uint_pattern.sub(new_uint, line, count=1)
            uint_fixes += 1
            break

    # ---------------------------------------------
    # 2. BITMAP COMMENT FIX
    # ---------------------------------------------
    elif choice == "2":
      bitmap_match = bitmap_pattern.search(line)
      if bitmap_match:
        glyph_index = int(bitmap_match.group(1))
        ascii_code = glyph_index + 32
        ascii_char = chr(ascii_code)
        expected = f"   // 0x{ascii_code:02X} '{ascii_char}'"
        line, missing_bitmap_comments, incorrect_bitmap_comments, exit_now = fix_glyph_comment(
          line,
          ascii_code,
          expected,
          comment_prefix,
          missing_bitmap_comments,
          incorrect_bitmap_comments,
          "Bitmap array"
        )
        if exit_now:
          fixed_lines.append(line)
          fixed_lines.extend(lines[line_index+1:])
          break

    # ---------------------------------------------
    # 3. FIX MISSING '0b' & 'UL'
    # ---------------------------------------------
    elif choice == "3":
      if re.search(r'\b[01]{3,}\b', line):
        parts = line.split(",")
        rebuilt = []
        for part in parts:
          token = part.strip()
          if not token:
            continue
          # ----- Extract only binary digits -----
          binary_digits = "".join(re.findall(r'[01]+', token))
          if not binary_digits:
            continue
          rebuilt.append(f"0b{binary_digits}UL")
          if f"0b{binary_digits}UL" != token:
            binary_repairs += 1
        if rebuilt:
          # ----- Prepare final line with 2-space indentation -----
          indented_line = "  "  # 2 spaces
          if len(rebuilt) == 1:
            indented_line += rebuilt[0] + "\n"
          else:
            indented_line += (", ".join(rebuilt[:-1]) + ", " + rebuilt[-1] + "\n")
          line = indented_line

    # ---------------------------------------------
    # 5. FIX MISSING 'pt7b'
    # ---------------------------------------------
    elif choice == "5":
      print("\n  Glyphy will not automate this repair.")
      print("  Reason: I am not sure if this is even needed for ProffieOS?")
      print("        Also, this is a quick and easy fix, if you want it.")
      print("\n  Do the following in your favorite text editor:")
      print("    Replace:  MyFontChar")
      print("    With:     MyFontpt7bChar")
      print("    Action:   Replace All, or one by one if your font is a 'real' mess")
      print("    Then save the file.")
      print("\n  You can do it.             MTFBWY")
      pt7b_additions += 0
      break

    # ---------------------------------------------
    # END OF FIRST PASS : BITMAP ARRAYS
    # ---------------------------------------------
    fixed_lines.append(line)

  # ==================================================
  # SECOND PASS : GLYPHDATA
  # ==================================================

  # ---------------------------------------------
  # 2. GLYPHDATA COMMENT FIX
  # ---------------------------------------------
  if choice == "2":
    new_lines = []
    for line_index, line in enumerate(fixed_lines):
      glyphdata_match = glyphdata_pattern.search(line)
      if glyphdata_match:
        glyph_index = int(glyphdata_match.group(2))
        ascii_code = glyph_index + 32
        ascii_char = chr(ascii_code)
        expected = f"   // 0x{ascii_code:02X} '{ascii_char}'"
        line, missing_glyphdata_comments, incorrect_glyphdata_comments, exit_now = fix_glyph_comment(
          line,
          ascii_code,
          expected,
          comment_prefix,
          missing_glyphdata_comments,
          incorrect_glyphdata_comments,
          "GLYPHDATA"
        )
        if exit_now:
          new_lines.append(line)
          new_lines.extend(fixed_lines[line_index+1:])
          break
      new_lines.append(line)
    fixed_lines = new_lines

  # ---------------------------------------------
  # 4. FIX MISSING GLYPHs (uses parser ctx) (bitmap array & GLYPHDATA)
  # ---------------------------------------------
  elif choice == "4":

    existing_bitmaps = set(ctx["bitmap_dict"].keys())
    existing_glyphdata = set(ctx["glyphdata_dict"].keys())
    all_indices = sorted(existing_bitmaps | existing_glyphdata)
    if not all_indices:
      return

    min_index = min(all_indices)
    max_index = max(all_indices)

    average_advance_width = ctx["metrics"]["average_advance_width"]
    average_y_offset = ctx["metrics"]["average_y_offset"]

    basename = os.path.splitext(os.path.basename(font_file))[0]

    # --------------------------------------------------
    # Build missing glyph block separately
    # --------------------------------------------------
    missing_block = []

    missing_block.append("/* ================= Glyphy auto-added missing glyphs =================\n")
    missing_block.append("   ====================================================================\n\n")
    missing_block.append("   These are placeholders for your missing bitmap arrays and GLYPHDATAs.\n")
    missing_block.append("   They are generic and will not look good if used as they are.\n")
    missing_block.append("   You will need to fix the 'art' and insert them in the right places.\n")
    missing_block.append("   --------------------------------------------------------------------\n")

    for glyph_index in range(min_index, max_index + 1):

      has_bitmap = glyph_index in existing_bitmaps
      has_glyphdata = glyph_index in existing_glyphdata
      ascii_code = glyph_index + 32
      ascii_char = chr(ascii_code)
      charname = f"{basename}pt7bChar{glyph_index}"

      # ----- add missing bitmap -----
      if not has_bitmap:
        missing_block.append(f"const uint8_t {charname}[] = {{   // 0x{ascii_code:02X} '{ascii_char}' Glyphy's placeholders\n}};\n")
        bitmap_additions += 1

      # ----- add missing glyphdata -----
      if not has_glyphdata:
        x_offset = 0
        missing_block.append(f"  {{{average_advance_width}, {x_offset}, {average_y_offset}, GLYPHDATA({charname})}},   // 0x{ascii_code:02X} '{ascii_char}' Glyphy's placeholders\n")
        glyphdata_additions += 1

    missing_block.append("   ====================================================================\n")
    missing_block.append("   ======================= End of missing glyphs ======================\n")
    missing_block.append("   ==================================================================== */\n\n")

    # --------------------------------------------------
    # Only insert if something was actually missing
    # --------------------------------------------------
    if bitmap_additions or glyphdata_additions:
      fixed_lines = missing_block + fixed_lines

  # ==================================================
  # SUMMARY
  # ==================================================

  print("\n  Glyphy repair summary:")
  print("  --------------------------------------")
  if choice == "1":
    if uint_fixes:
      print(f"  uint fixes: {uint_fixes}")
    else:
      print("  No uint fixes needed. Types already correct.")
  if choice == "2":
    if missing_bitmap_comments:
      print(f"  Missing bitmap array comments added: {missing_bitmap_comments}")
    if incorrect_bitmap_comments:
      print(f"  Incorrect bitmap array comments replaced: {incorrect_bitmap_comments}")
    if missing_glyphdata_comments:
      print(f"  Missing GLYPHDATA comments added: {missing_glyphdata_comments}")
    if incorrect_glyphdata_comments:
      print(f"  Incorrect GLYPHDATA comments replaced: {incorrect_glyphdata_comments}")
    if not (missing_bitmap_comments or incorrect_bitmap_comments or missing_glyphdata_comments or incorrect_glyphdata_comments):
      print("  All comments look perfect. Glyphy found nothing to fix.")
  if choice == "3":
    if binary_repairs:
      print(f"  Binary syntax repairs: {binary_repairs}")
    else:
      print("  Binary syntax already clean. No repairs needed.")
  if choice == "4":
    if bitmap_additions:
      print(f"  Missing bitmap array additions: {bitmap_additions}")
    if glyphdata_additions:
      print(f"  Missing GLYPHDATA additions: {glyphdata_additions}")
    if not (bitmap_additions or glyphdata_additions):
      print("  All bitmap arrays and GLYPHDATAs are already present and accounted for.")
  if choice == "5":
    print(f"  pt7b additions: {pt7b_additions}")
    print("\n  Glyphy won't, but you can do it. Glyphy believes in you!")

  # ==================================================
  # WRITE CLONE
  # ==================================================

  if (
    uint_fixes or
    missing_bitmap_comments or
    incorrect_bitmap_comments or
    missing_glyphdata_comments or
    incorrect_glyphdata_comments or
    binary_repairs or
    bitmap_additions or
    glyphdata_additions or
    pt7b_additions
  ):
    with open(clone_path, "w", encoding="utf-8") as f:
      f.writelines(fixed_lines)
    print(f"\n  Repaired cloned font written to: {clone_path}")
  else:
    print("\n  No repairs were necessary. No clone created.")

  return

# ==================================================
# MAIN ENTRY POINT
# ==================================================

def main():
  """
  Program entry point.

  Flow:
    - Validate CLI arguments
    - Parse font file
    - Render glyphs image
    - Save image to OUTPUT_DIR
    - Save report/analysis to OUTPUT_DIR
  """

  os.makedirs(OUTPUT_DIR, exist_ok=True)

  if len(sys.argv) < 2:
    print("\n  Usage: python glyphy.py YourFont.h")
    print("  Exiting script.")
    print("                                           MTFBWY")
    sys.exit(1)

  font_file = sys.argv[1]
  font_obj, font_height, font_size, font_path = load_label_font()

  base_name = os.path.splitext(os.path.basename(font_file))[0]
  output_name = generate_output_name(base_name)

  # --------------------------------------------------
  # Skeleton prompt if file missing
  # --------------------------------------------------
  if not os.path.exists(font_file):

    answer = input(
      "\n  This font does not exist in this folder. Would you like to generate a skeleton for it? (y/n): "
    ).strip().lower()

    if answer in ("y", "yes"):
      create_skeleton_font(font_file)
      print("\n  Skeleton font created, exiting script.")
      print("                                           MTFBWY")
    else:
      print("\n  Exiting script. Please try again with an existing")
      print("              ProffieOS text font file.")
      print("                                             MTFBWY")

    return

  # --------------------------------------------------
  # Parse font
  # --------------------------------------------------
  _, dict_btmp_gdat = inner_core_critical_hit(GET_BTMP_GDAT)
  ctx = parse_font_file(font_file, dict_btmp_gdat)

  glyph_records = ctx["glyph_records"]
  metrics = ctx["metrics"]
  average_bitmap_width = metrics["average_bitmap_width"]

  if not glyph_records:
    print("No glyphs found.")
    sys.exit(1)

  # --------------------------------------------------
  # Geometry idiot-proofing protection
  # --------------------------------------------------
  global SCALE, DISPLAY_WIDTH, DISPLAY_HEIGHT, OUTER_WHITE_BORDER, INNER_BLACK_BORDER, SPACING

  # ----- if these are changed below the minimum threshold, geometry will break and GLYPHY too -----
  SCALE = max(1, int(SCALE))
  DISPLAY_WIDTH = max(32, int(DISPLAY_WIDTH))
  DISPLAY_HEIGHT = max(32, int(DISPLAY_HEIGHT))
  OUTER_WHITE_BORDER = max(0, int(OUTER_WHITE_BORDER))
  INNER_BLACK_BORDER = max(0, int(INNER_BLACK_BORDER))
  SPACING = max(0, int(SPACING))

  # --------------------------------------------------
  # Render image
  # --------------------------------------------------
  if RENDER_MODE == "table" or RENDER_MODE == "text":
    img = render_glyphs(glyph_records, average_bitmap_width)

    output_path = os.path.join(OUTPUT_DIR, output_name)
    img.save(output_path)
    print(f"\n  Saved render: /{OUTPUT_DIR}/{output_name}")

    # --------------------------------------------------
    # Write report (same numbering)
    # --------------------------------------------------
    ctx["diagnostics"]["total_bg_errors"]["enabled"] = (GEOMETRY_TAMPERED or FORCE_CORE_BREACH_EVENT)
    if ENABLE_DEVELOPER_DEBUG_MODE:
      import pprint
      base = os.path.splitext(output_name)[0]
      ctx_name = f"{base}_ctx.txt"
      ctx_path = os.path.join(OUTPUT_DIR, ctx_name)
      with open(ctx_path, "w", encoding="utf-8") as f:
        pprint.pprint(ctx, stream=f, width=120, sort_dicts=False)
      print(f"\n  Saved ctx: /{OUTPUT_DIR}/{os.path.basename(ctx_path)}")

    report_path = write_report_file(
      output_name,
      font_file,
      ctx,
      font_path,
      font_size,
      font_height
    )

    if GENERATE_REPORT:
      print(f"\n  Saved report: /{OUTPUT_DIR}/{os.path.basename(report_path)}")

    if AUTO_OPEN_IMAGE:
      open_file(output_path)

  # --------------------------------------------------
  # Random/single bitmap mode
  # --------------------------------------------------
  elif ( RENDER_MODE == "random" and LOOK_FOR ) or ( RENDER_MODE == "this" and THIS ):
    img, report = render_single_bitmap(font_file, output_name)
    if img:
      output_path = os.path.join(OUTPUT_DIR, output_name)
      img.save(output_path)
      print(f"\n  Saved render: /{OUTPUT_DIR}/{output_name}")
      if AUTO_OPEN_IMAGE:
        open_file(output_path)
    if report:
      if GENERATE_REPORT and AUTO_OPEN_REPORT:
        open_file(report)
    return
  else:
    print('\n  Invalid RENDER_MODE, please select "table", "text", "random" or "this".')
    return

  # --------------------------------------------------
  # Run font "fix-it" tools
  # --------------------------------------------------
  def timed_input(prompt, timeout=60, default="n"):
    """
    Prompt user with a countdown timer displayed in the console.
    Returns user input or default after timeout.
    """

    result = {"value": default}
    def ask():
      try:
        result["value"] = input("")  # just read input silently
      except EOFError:
        pass
    t = threading.Thread(target=ask)
    t.daemon = True
    t.start()
    start_time = time.time()
    while t.is_alive():
      elapsed = int(time.time() - start_time)
      remaining = timeout - elapsed
      if remaining <= 0:
        break
      sys.stdout.write(f"\r{prompt}  [{remaining:02d}s] ")
      sys.stdout.flush()
      time.sleep(1)
    if t.is_alive():
      print(f"\n  No response within {timeout} seconds → assuming '{default}'.")
      return default
    # ----- User entered something -----
    return (result["value"] or default).strip().lower()

  severity = ctx["severity_totals"]
  has_problems = ( severity["error"] > 0 or severity["warning"] > 0 )

  if has_problems:
    print("\n  Font issues detected.")
    print("  --------------------------------------")
    if OPEN_REPAIR_MENU:
      answer = timed_input("  Launch repair tools? (y/n): ", timeout=60, default="n")
      if answer.startswith("y"):
        run_repair_menu(font_file, ctx)
    else:
      print("  Please set OPEN_REPAIR_MENU to True to run repair menu.")

if __name__ == "__main__":
  main()
