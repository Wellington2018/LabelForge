"""
generator.py

Responsável pela geração das etiquetas em formato ODT.

Autor: Wellington Oliveira
Projeto: LabelForge
"""

from pathlib import Path

from odf.opendocument import load

from models import Produto, ModeloEtiqueta
from utils import gerar_nome_saida


class ODTGenerator:
    """
    Gera um documento ODT substituindo os marcadores pelos
    dados dos produtos.
    """

    def __init__(
        self,
        modelo: ModeloEtiqueta,
        pasta_saida: Path,
    ):
        self.modelo = modelo
        self.pasta_saida = pasta_saida

    # ==========================================================
    # MÉTODOS PRIVADOS
    # ==========================================================

    def _substituir_texto(self, elemento, substituicoes):
        """
        Percorre toda a árvore XML do documento ODT e substitui
        os marcadores encontrados.
        """

        if hasattr(elemento, "data"):

            texto = elemento.data

            for marcador, valor in substituicoes.items():
                texto = texto.replace(marcador, valor)

            elemento.data = texto

        if hasattr(elemento, "childNodes"):

            for filho in elemento.childNodes:
                self._substituir_texto(
                    filho,
                    substituicoes,
                )

    def _criar_substituicoes(
        self,
        produtos: list[Produto],
    ) -> dict:
        """
        Converte a lista de produtos em um dicionário de
        marcadores.
        """

        substituicoes = {}

        for indice, produto in enumerate(produtos, start=1):

            if indice > self.modelo.limite:
                break

            substituicoes[f"{{{{CODIGO{indice}}}}}"] = produto.codigo
            substituicoes[f"{{{{PRODUTO{indice}}}}}"] = produto.nome
            substituicoes[f"{{{{PRECO{indice}}}}}"] = produto.preco

        return substituicoes

    # ==========================================================
    # MÉTODO PÚBLICO
    # ==========================================================

    def gerar(
        self,
        produtos: list[Produto],
    ) -> Path:
        """
        Gera o arquivo ODT e retorna o caminho do documento.
        """

        documento = load(str(self.modelo.arquivo))

        substituicoes = self._criar_substituicoes(produtos)

        self._substituir_texto(
            documento.text,
            substituicoes,
        )

        arquivo_saida = gerar_nome_saida(
            self.modelo.nome,
            self.pasta_saida,
        )

        documento.save(str(arquivo_saida))

        return arquivo_saida
