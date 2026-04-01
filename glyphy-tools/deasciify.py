"""
Usage:

python deasciify.py

"""

# deasciify.py
# Convert ASCII back + rotate CW (derotate)

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

  # ----- remove empty lines -----
  lines = [line for line in lines if line.strip()]

  # ----- re-pad to rectangle -----
  max_line_length = max(len(line) for line in lines)

  grid = []
  for line in lines:
    padded = line.ljust(max_line_length, " ")
    grid.append(list(padded))

  return grid


def deasciify(grid):
  result = []

  for row in grid:
    new_row = []
    for character in row:
      if character == "█":
        new_row.append("1")
      elif character == " ":
        new_row.append("0")
      else:
        new_row.append(character)
    result.append(new_row)

  return result

def rotate_cw(grid):
  height = len(grid)
  width = len(grid[0])

  rotated = []
  for column_index in range(width):
    new_row = []
    for row_index in range(height - 1, -1, -1):
      new_row.append(grid[row_index][column_index])
    rotated.append(new_row)

  return rotated

def write_output(grid):
  with open("deasciified.txt", "w", encoding="utf-8") as output_file:
    for row_index, row in enumerate(grid):
      line = "".join(row).rstrip()

      if row_index == len(grid) - 1:
        output_file.write("  " + line + "\n")
      else:
        output_file.write("  " + line + ",\n")

    # ----- determine height from bit length -----
    if grid:
      glyph_height = len(grid[0])
    else:
      glyph_height = 0

    glyph_width = len(grid)

    # ----- determine uintXX_t required -----
    if glyph_height <= 8:
      required = 8
    elif glyph_height <= 16:
      required = 16
    else:
      required = 32

    output_file.write("\n")
    output_file.write(f"  uint{required}_t\n")
    output_file.write(f"\n  Glyph height: {glyph_height}")
    output_file.write(f"\n  Glyph width: {glyph_width}")

def main():
  grid = read_grid("asciified.txt")

  if grid is None:
    return

  binary_grid = deasciify(grid)
  rotated = rotate_cw(binary_grid)
  write_output(rotated)

  print("\n  De-asciified & derotated output written to deasciified.txt\n")
  print("\n                                                           MTFBWY")

  open_file("deasciified.txt")

if __name__ == "__main__":
  main()
