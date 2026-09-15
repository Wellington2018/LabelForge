import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).resolve().parent
else:
    ROOT_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
TEMPLATES_DIR = ROOT_DIR / "templates"

INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

MODELOS = {
    "1": {
        "nome": "10x1",
        "arquivo": TEMPLATES_DIR / "10X1.odt",
        "limite": 10,
    },
    "2": {
        "nome": "24x1",
        "arquivo": TEMPLATES_DIR / "24X1.odt",
        "limite": 24,
    },
    "3": {
        "nome": "A4",
        "arquivo": TEMPLATES_DIR / "A4.odt",
        "limite": 10,
    },
    "4": {
        "nome": "A5",
        "arquivo": TEMPLATES_DIR / "A5.odt",
        "limite": 10,
    },
}