"""
Usage:

python rotate_flips.py

"""
# apply flips and or rotations


import os
import platform
import subprocess

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
ROTATION   = 180         # Accepted values: 0, 90 (for CW), -90 (for CCW), 180 or 270.
FLIP_TOP_BOTTOM = False  # what I call horizontal flip
FLIP_LEFT_RIGHT = False  # what I call vertical flip

GLYPH = """
  0b0000000000010100100000UL,
  0b0000000100010010100010UL,
  0b0000000010011111110100UL,
  0b0000000001110000011000UL,
  0b0000001001100000001101UL,
  0b0000011111000111000110UL,
  0b0000000000001111100100UL,
  0b1111111110001111100111UL,
  0b0000000000001111100100UL,
  0b0000011011000111000100UL,
  0b0000001111100000001111UL,
  0b0000000001110000011000UL,
  0b0000000001011111111100UL,
  0b0000000010010110100010UL,
  0b0000000100010010100000UL,
  0b0000000000100100010000UL
"""

# --------------------------------------------------
# OPEN FILE HELPER
# --------------------------------------------------
def open_file(file_path):
  operating_system = platform.system()

  try:
    if operating_system == "Windows":
      os.startfile(file_path)
    elif operating_system == "Darwin":
      subprocess.run(["open", file_path])
    else:
      subprocess.run(["xdg-open", file_path])
  except Exception as error:
    print(f"Could not open file automatically: {error}")

# --------------------------------------------------
# PARSE GLYPH → CLEAN GRID
# --------------------------------------------------
def parse_glyph(text):
  lines = text.splitlines()

  # remove empty lines
  lines = [line.strip() for line in lines if line.strip()]

  grid = []

  for line in lines:
    line = line.rstrip(",")

    # remove prefix/suffix
    if line.startswith("0b"):
      line = line[2:]
    if line.endswith("UL"):
      line = line[:-2]

    grid.append(list(line))

  return grid

# --------------------------------------------------
# TRANSFORMATIONS
# --------------------------------------------------
def apply_flips(grid):
  """
  Apply optional horizontal and/or vertical flips
  to a grid according to global settings.

  Returns:
    Transformed grid.
  """
  if FLIP_LEFT_RIGHT:
    grid = [row[::-1] for row in grid]
  if FLIP_TOP_BOTTOM:
    grid = grid[::-1]
  return grid

def apply_rotation(grid):
  """
  Rotate grid according to ROTATION setting.

  Accepted values:
    0     → no rotation
    90    → clockwise (CW)
    180   → upside down
    -90   → counter-clockwise (CCW)
    270   → same as -90

  Returns:
    Rotated grid.

  Raises:
    ValueError if ROTATION is invalid.
  """
  if ROTATION == 0:
    return grid
  if ROTATION == 90:
    return [list(row) for row in zip(*grid[::-1])]
  if ROTATION in (-90, 270):
    return [list(row) for row in zip(*grid)][::-1]
  if ROTATION == 180:
    return [row[::-1] for row in grid[::-1]]
  raise ValueError("\n  Invalid ROTATION value, must be 0, 90, -90, 180, or 270")

# --------------------------------------------------
# WRITE OUTPUT
# --------------------------------------------------
def write_output(grid):
  with open("rotated_flipped.txt", "w", encoding="utf-8") as output_file:

    for row_index, row in enumerate(grid):
      line = "".join(row)

      # add back prefix/suffix
      line = "0b" + line + "UL"

      if row_index < len(grid) - 1:
        output_file.write(f"  {line},\n")
      else:
        output_file.write(f"  {line}\n")

# --------------------------------------------------
# CLI MAIN ENTRY POINT
# --------------------------------------------------
def main():
  grid = parse_glyph(GLYPH)

  if not grid:
    print("\n  Empty GLYPH.")
    return

  flipped_grid = apply_flips(grid)
  rotated_grid = apply_rotation(flipped_grid)
  write_output(rotated_grid)

  print("\n  Rotated output written to rotated_flipped.txt\n")

  open_file("rotated_flipped.txt")

if __name__ == "__main__":
  main()
