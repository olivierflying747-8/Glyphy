"""
Usage:

python deasciify.py

"""

# deasciify.py
# Convert ASCII back + rotate CW (derotate)

import re
import os
import platform
import subprocess

def open_file(file_path):
  operating_system = platform.system()

  try:
    # ----- Windows -----
    if operating_system == "Windows":
      os.startfile(file_path)
    # ----- macOS -----
    elif operating_system == "Darwin":
      subprocess.run(["open", file_path])
    # ----- Linux / Unix (xdg-open) -----
    else:
      subprocess.run(["xdg-open", file_path])

  except Exception as error:
    print(f"Could not open file automatically: {error}")

def read_grid(file_path):
  if not os.path.exists(file_path):
    print("Error: asciified.txt not found.")
    return None

  with open(file_path, "r", encoding="utf-8") as input_file:
    lines = [line.rstrip("\n") for line in input_file]

  # ----- DO NOT remove anything — keep structure intact -----
  return [list(line) for line in lines]

def deasciify(grid):
  """
  Convert visual ASCII grid into binary grid (still as list of lists).
  Keeps structure intact.
  """
  binary_grid = []

  for row in grid:
    binary_row = []

    for character in row:
      if character == "█":
        binary_row.append("1")
      elif character == " ":
        binary_row.append("0")
      else:
        binary_row.append(character)  # keep 0b / UL / anything else

    binary_grid.append(binary_row)

  return binary_grid

def pad_grid(grid):
  """
  Pad all rows to equal length using '0'
  """
  max_width = max(len(row) for row in grid)

  padded_grid = []
  for row in grid:
    padded_row = row + ["0"] * (max_width - len(row))
    padded_grid.append(padded_row)

  return padded_grid

def derotate_grid(grid):  # rotate CW
  """
  Rotate clockwise (reverse of asciify rotation)
  """
  height = len(grid)
  width = len(grid[0])

  rotated_grid = []

  for column_index in range(width):
    new_row = []
    for row_index in range(height - 1, -1, -1):
      new_row.append(grid[row_index][column_index])

    rotated_grid.append(new_row)

  return rotated_grid

def measure_glyph(grid):
  """
  Measure width and height from binary grid
  """

  # width = number of rows (columns in bitmap)
  glyph_width = len(grid)

  if not grid:
    return 0, 0

  # reconstruct first line as string
  first_row_string = "".join(grid[0]).strip().rstrip(",")

  # remove prefix/suffix if present
  if first_row_string.startswith("0b"):
    first_row_string = first_row_string[2:]

  if first_row_string.endswith("UL"):
    first_row_string = first_row_string[:-2]

  # height = number of bits
  glyph_height = sum(1 for character in first_row_string if character in ("0", "1"))

  return glyph_width, glyph_height

def write_output(grid):
  """
  Convert grid rows into '0b...UL' strings
  Final formatting + metadata
  """
  output_lines = []

  for row in grid:
    line = "".join(row).strip()

    # remove existing prefix/suffix if present
    if not line.startswith("0b"):
      line = "0b" + line
    if not line.endswith("UL"):
      line = line + "UL"

    output_lines.append(line)

  glyph_width, glyph_height = measure_glyph(grid)

    # ----- determine uintXX_t required -----
  if glyph_height <= 8:
    required_uint = 8
  elif glyph_height <= 16:
    required_uint = 16
  elif glyph_height <= 32:
    required_uint = 32
  else:
    required_uint = glyph_height

  with open("deasciified.txt", "w", encoding="utf-8") as output_file:

    for line_index, line_text in enumerate(output_lines):
      if line_index < len(output_lines) - 1:
        output_file.write(f"  {line_text},\n")
      else:
        output_file.write(f"  {line_text}\n")

    output_file.write("\n")
    output_file.write(f"  uint{required_uint}_t\n")
    if required_uint > 32:
      output_file.write("    WARNING height is greater than 32px, it will not fit on standard OLED 128x32.\n")
    output_file.write(f"\n  Glyph height: {glyph_height}")
    output_file.write(f"\n  Glyph width: {glyph_width}")

def main():
  grid = read_grid("asciified.txt")

  if grid is None:
    return

  binary_grid = deasciify(grid)
  padded_grid = pad_grid(binary_grid)
  derotated_grid = derotate_grid(padded_grid)
  write_output(derotated_grid)

  print("\n  De-asciified & derotated output written to deasciified.txt\n")
  print("\n                                                           MTFBWY")

  open_file("deasciified.txt")

if __name__ == "__main__":
  main()
