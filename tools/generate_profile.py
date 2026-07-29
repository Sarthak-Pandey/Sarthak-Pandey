import sys
from pathlib import Path

# Add workspace src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from living_terminal.cli import main

if __name__ == "__main__":
    main()
