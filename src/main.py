"""
main.py

Ponto de entrada do LabelForge.

Autor: Wellington Oliveira
Projeto: LabelForge
"""

from pathlib import Path

from config import INPUT_DIR, OUTPUT_DIR, MODELOS
from generator import ODTGenerator
from models import ModeloEtiqueta
from parser import PDFParser
from utils import titulo, validar_arquivo


def escolher_modelo() -> ModeloEtiqueta:
    """
    Exibe o menu e retorna o modelo escolhido.
    """

    print("\nModelos disponíveis:\n")

    for codigo, modelo in MODELOS.items():
        print(f"{codigo} - Modelo {modelo['nome']}")

    while True:

        opcao = input("\nEscolha o modelo: ").strip()

        if opcao in MODELOS:

            dados = MODELOS[opcao]

            return ModeloEtiqueta(
                nome=dados["nome"],
                arquivo=dados["arquivo"],
                limite=dados["limite"],
            )

        print("Opção inválida!")


def localizar_pdf() -> Path:
    """
    Procura automaticamente um PDF dentro da pasta input.

    Caso exista mais de um PDF, utiliza o primeiro encontrado.
    """

    arquivos = sorted(INPUT_DIR.glob("*.pdf"))

    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum PDF encontrado em:\n{INPUT_DIR.resolve()}"
        )

    return arquivos[0]


def main():

    titulo("LABELFORGE")

    try:

        pdf = localizar_pdf()

        validar_arquivo(pdf)

        modelo = escolher_modelo()

        validar_arquivo(modelo.arquivo)

        print("\nLendo orçamento...")

        parser = PDFParser(pdf)

        produtos = parser.extrair_produtos()

        if not produtos:
            print("\nNenhum produto encontrado.")
            return

        print(f"\n{len(produtos)} produto(s) encontrado(s).\n")

        for indice, produto in enumerate(produtos, start=1):

            print(
                f"{indice:02d} | "
                f"{produto.codigo} | "
                f"{produto.nome} | "
                f"{produto.preco}"
            )

        print("\nGerando etiquetas...")

        gerador = ODTGenerator(
            modelo=modelo,
            pasta_saida=OUTPUT_DIR,
        )

        arquivo = gerador.gerar(produtos)

        print("\nArquivo gerado com sucesso!")

        print(f"\n{arquivo}")

    except Exception as erro:

        print("\nERRO")

        print("-" * 60)

        print(erro)


if __name__ == "__main__":
    main()
