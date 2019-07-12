from pathlib import Path
import os

home = Path.home

# os.makedirs()
print(os.path.exists(str(Path.home()) + "/.config/mgtow-archive"))
print()
