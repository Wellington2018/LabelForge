"""
utils.py

Funções auxiliares utilizadas por todo o projeto.
"""

from datetime import datetime
from pathlib import Path


def gerar_nome_saida(modelo: str, pasta_saida: Path) -> Path:
    """
    Gera um nome único para o arquivo de saída.

    Exemplo:
        Etiquetas_10x1_27-07-2026_15-30-12.odt
    """

    nome = datetime.now().strftime(
        f"Etiquetas_{modelo}_%d-%m-%Y_%H-%M-%S.odt"
    )

    return pasta_saida / nome


def validar_arquivo(caminho: Path) -> None:
    """
    Verifica se um arquivo existe.

    Levanta FileNotFoundError caso não exista.
    """

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado:\n{caminho.resolve()}"
        )


def linha():
    """
    Imprime uma linha separadora.
    """

    print("-" * 60)


def titulo(texto: str):
    """
    Exibe um título formatado.
    """

    linha()
    print(texto)
    linha()
