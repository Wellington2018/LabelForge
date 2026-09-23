from datetime import datetime
from pathlib import Path


def gerar_nome_saida(modelo: str, pasta_saida: Path) -> Path:

    nome = datetime.now().strftime(
        f"Etiquetas_{modelo}_%d-%m-%Y_%H-%M-%S.odt"
    )

    return pasta_saida / nome


def validar_arquivo(caminho: Path) -> None:

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado:\n{caminho.resolve()}"
        )


def linha():

    print("-" * 60)


def titulo(texto: str):

    linha()
    print(texto)
    linha()
