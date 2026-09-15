from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Produto:
    codigo: str
    nome: str
    preco: str


@dataclass(slots=True)
class ModeloEtiqueta:
    nome: str
    arquivo: Path
    limite: int