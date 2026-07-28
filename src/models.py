"""
models.py

Contém as classes que representam os objetos do sistema.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Produto:
    """
    Representa um produto encontrado no orçamento.
    """

    codigo: str
    nome: str
    preco: str


@dataclass(slots=True)
class ModeloEtiqueta:
    """
    Representa um modelo de etiqueta.
    """

    nome: str
    arquivo: Path
    limite: int
