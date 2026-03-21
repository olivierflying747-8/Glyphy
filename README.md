# Glyphy is a CLI Python script based project that renders & analyses ProffieOS .h text font files.

It generates:<br>
- A visual preview image (.bmp, .png or .jpg)<br>
- A detailed analysis report (optional with `GENERATE_REPORT = True`)

## Glyphy's Missions:

1. Visualizer:<br>
Render everything drawable from a ProffieOS .h text font file.<br>
  Glyphy will show you every duplicate, every forgotten commented ghosts.<br>
  You can have as many bitmap arrays and/or GLYPHDATA as you like,<br>
  Glyphy will show them all.<br>
  Glyphy will even show you what is "not there" with color coded glyphs:<br>
  - Yellow: missing GLYPHDATA
  - Orange: missing bitmap arrays / empty bitmap arrays
  - Red:    missing both
  - Grey:   duplicates<br>
  Labels follow the same logic except if a duplicate is not commented, then it will be Red

2. Validator:<br>
The validator reports many deviations.<br>
  For example: incorrect uintXX_t number, missing bitmap array / GLYPHDA / both<br>
  Several "deviations" are for information only, some glyphs are designed to "move weirdly" (many in the case of StarJedi10Font.h)

3. Limited Repair System:<br>
Provide automated tools to repair structural or cosmetic font issues.<br>
  For example: fix incorrect uintXX_t numbers, add ASCII comments for each bitmap array and GLYPHDATA<br>
  - Glyphy cannot generate missing "glyph-art"
  - Glyphy will not modify the original, but will generate a repaired clone
  - Glyphy will not overwrite clones, a new clone will be created

## Rendered Examples:<br>
StarJedi10Font.h, `RENDER_MODE = "text", DISPLAY_DIAGNOSTIC = False, ROW_ALIGN = "center"`<br>
<p align="center">
  <img src="RenderedExamples/StarJedi10Font_03.jpg">
</p>

Aurebesh10Font.h, `RENDER_MODE = "table", DISPLAY_DIAGNOSTIC = True, ROW_ALIGN = "left"`<br>
<p align="center">
  <img src="RenderedExamples/Aurebesh10Font_02.png" width="50%">
</p>

saber_logo.h, `RENDER_MODE = "random",  DISPLAY_DIAGNOSTIC = True`<br>
<p align="center">
  <img src="RenderedExamples/saber_logo_01.png">
</p>

OLED sized logo, `RENDER_MODE = "text", BLACK_AND_WHITE_ONLY = True, ROW_ALIGN = "center"`<br>
<table align="center">
  <tr>
    <td align="center">
      <b>INVERT_BLACK_AND_WHITE = True</b><br>
      <img src="RenderedExamples/StarJedi10Font_05.jpg">
    </td>
    <td align="center">
      <b>INVERT_BLACK_AND_WHITE = False</b><br>
      <img src="RenderedExamples/StarJedi10Font_04.jpg">
    </td>
  </tr>
</table>

## OS:
- tested on Windows
- should be compatible with:
  - macOS
  - Linux/Unix

## Requirements:

- Python 3.9 or newer
- Pillow (Python Imaging Library)

See [`InstallationGuide/InstallationGuide.md`](InstallationGuide/InstallationGuide.md) for a quick Glyphy & Python install guide.
