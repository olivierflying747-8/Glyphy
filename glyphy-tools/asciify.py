"""
Usage:

python asciify.py

"""

# asciify.py
# Rotate CCW + convert to ASCII visualization

GLYPH = """
  0b000000000000000000UL,
  0b000001111111100000UL,
  0b000111000000111000UL,
  0b001101111111101100UL,
  0b011011111111110110UL,
  0b010011011110110010UL,
  0b100111101101111011UL,
  0b101111100001111101UL,
  0b101111000000111101UL,
  0b111100000000001111UL,
  0b101111000000111101UL,
  0b100111100001111001UL,
  0b010111101101111011UL,
  0b010011011110110010UL,
  0b001011111111110100UL,
  0b000101111111101000UL,
  0b000011000000110000UL,
  0b000001111111100000UL,
"""

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

def validate_rectangularity(lines):
  if not lines:
    print("\n  Error: GLYPH is empty.")
    return False

  expected_length = len(lines[0])
  mismatch_found = False

  print("")  # spacing

  for line_index, line in enumerate(lines):
    current_length = len(line)

    if current_length != expected_length:
      if not mismatch_found:
        print("  Error: GLYPH is not rectangular.\n")
        print(f"  Expected length (line 1): {expected_length}\n")

      print(f"  Line {line_index + 1} length: {current_length}")
      mismatch_found = True

  if mismatch_found:
    print("\n  Please fix GLYPH before running asciify.py again.")
    return False

  return True

def build_grid(text):
  lines = text.splitlines()

  while lines and lines[0].strip() == "":
    lines.pop(0)
  while lines and lines[-1].strip() == "":
    lines.pop()

  processed_lines = []

  for line in lines:
    line = line.strip()

    if line.endswith(","):
      line = line[:-1]

    processed_lines.append(line)

  # ----- validate BEFORE transformation -----
  if not validate_rectangularity(processed_lines):
    return None

  grid = []

  for line in lines:

    # ----- split into parts -----
    prefix = ""
    suffix = ""

    if line.startswith("0b"):
      prefix = "0b"
      line = line[2:]

    if line.endswith("UL"):
      suffix = "UL"
      line = line[:-2]

    # ----- convert bitmap only -----
    converted = ""
    for character in line:
      if character == "1":
        converted += "█"
      elif character == "0":
        converted += " "
      else:
        converted += character

    new_line = prefix + converted + suffix
    grid.append(list(new_line))

  return grid

def rotate_ccw(grid):
  height = len(grid)
  width = len(grid[0])

  rotated = []
  for column_index in range(width - 1, -1, -1):
    new_row = []
    for row_index in range(height):
      new_row.append(grid[row_index][column_index])
    rotated.append(new_row)

  return rotated

def write_output(grid):
  with open("asciified.txt", "w", encoding="utf-8") as output_file:
    for row in grid:
      output_file.write("".join(row).rstrip() + "\n")


def main():
  grid = build_grid(GLYPH)

  if grid is None:
    return

  rotated = rotate_ccw(grid)
  write_output(rotated)

  print("\n  Asciified & rotated output written to asciified.txt\n")
  print("\n                                                           MTFBWY")

  open_file("asciified.txt")

if __name__ == "__main__":
  main()
