# Installation Guide
1️ Install Python
================

- Download Python from: https://www.python.org/downloads/
- During installation: Make sure "Add Python to PATH" is checked.
- Verify installation: python --version
- You should see something like: Python 3.11.x

2️ Install Pillow
================

- Open a terminal (Command Prompt / PowerShell / Terminal):
- pip install pillow

3️ Download Glyphy
=================

Download ZIP from GitHub:
- Click "Code"
- Click "Download ZIP"
- Extract the folder

▶ Running Glyphy
-----------------

- Navigate to the folder containing glyphy.py<br>
  Example: cd path/to/glyphy
- Run:<br>
python glyphy.py YourFont.h

Where To Place Glyphy? You have two options:
-----------------

Option A — Keep Glyphy in its own folder<br>
Place .h font files inside that folder before running.

Option B — Place Glyphy inside: ProffieOS/display/<br>
Then run it directly on fonts already located there.

Glyphy generates:
-----------------

FontName_01.bmp or .png or .jpg<br>
FontName_01_Analysis.txt (optional detailed validation report)<br>
Output files are saved inside: glyphy_outputs/

Rendering Modes
-----------------

Edit settings inside glyphy.py:

RENDER_MODE = "table"  → Render full font<br>
RENDER_MODE = "text"   → Render custom string<br>
RENDER_MODE = "random" → Render a single bitmap from a .h file (not a text font)<br>

Advanced:
-----------------
- Custom scaling
- Diagnostic grid overlays
- Missing character highlighting
- Width wrapping
- Baseline & cap-height visualization
- much much more

All configurable at the top of the script.
