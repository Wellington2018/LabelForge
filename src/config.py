"""
config.py

Centraliza todas as configurações do projeto.
"""

from pathlib import Path

# ============================================================
# PASTAS
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
TEMPLATES_DIR = ROOT_DIR / "templates"

OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# MODELOS DISPONÍVEIS
# ============================================================

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
}
