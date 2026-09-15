from pathlib import Path
import re

from odf.opendocument import load

from models import Produto, ModeloEtiqueta
from utils import gerar_nome_saida


class ODTGenerator:

    def __init__(
        self,
        modelo: ModeloEtiqueta,
        pasta_saida: Path,
    ):
        self.modelo = modelo
        self.pasta_saida = pasta_saida

    def _obter_nos_texto(self, elemento):
        nos = []

        if hasattr(elemento, "data"):
            nos.append(elemento)

        if hasattr(elemento, "childNodes"):
            for filho in elemento.childNodes:
                nos.extend(
                    self._obter_nos_texto(filho)
                )

        return nos

    def _substituir_marcadores(self, elemento, substituicoes):
        if not hasattr(elemento, "childNodes"):
            return

        for filho in elemento.childNodes:
            self._substituir_marcadores(
                filho,
                substituicoes,
            )

        nos = self._obter_nos_texto(elemento)

        if not nos:
            return

        while True:
            texto_completo = "".join(
                no.data
                for no in nos
            )

            encontrado = None

            for marcador, valor in substituicoes.items():
                posicao = texto_completo.find(marcador)

                if posicao != -1:
                    encontrado = (
                        marcador,
                        valor,
                        posicao
                    )
                    break

            if encontrado is None:
                break

            marcador, valor, posicao = encontrado

            inicio = posicao
            fim = posicao + len(marcador)

            indice_inicio = 0
            indice_fim = 0
            deslocamento_inicio = 0
            deslocamento_fim = 0

            acumulado = 0

            for indice, no in enumerate(nos):
                proximo = acumulado + len(no.data)

                if inicio >= acumulado and inicio < proximo:
                    indice_inicio = indice
                    deslocamento_inicio = inicio - acumulado

                if fim > acumulado and fim <= proximo:
                    indice_fim = indice
                    deslocamento_fim = fim - acumulado
                    break

                acumulado = proximo

            if indice_inicio == indice_fim:
                no = nos[indice_inicio]

                no.data = (
                    no.data[:deslocamento_inicio]
                    + valor
                    + no.data[deslocamento_inicio + len(marcador):]
                )

            else:
                primeiro = nos[indice_inicio]
                ultimo = nos[indice_fim]

                prefixo = primeiro.data[:deslocamento_inicio]
                sufixo = ultimo.data[deslocamento_fim:]

                primeiro.data = (
                    prefixo
                    + valor
                    + sufixo
                )

                for indice in range(
                    indice_inicio + 1,
                    indice_fim + 1
                ):
                    if indice != indice_fim:
                        nos[indice].data = ""
                    else:
                        nos[indice].data = ""

    def _criar_substituicoes(
        self,
        produtos: list[Produto],
    ) -> dict:
        substituicoes = {}

        for indice in range(
            1,
            self.modelo.limite + 1
        ):
            substituicoes[
                f"{{{{CODIGO{indice}}}}}"
            ] = ""

            substituicoes[
                f"{{{{PRODUTO{indice}}}}}"
            ] = ""

            substituicoes[
                f"{{{{PRECO{indice}}}}}"
            ] = ""

        for indice, produto in enumerate(
            produtos,
            start=1
        ):
            if indice > self.modelo.limite:
                break

            substituicoes[
                f"{{{{CODIGO{indice}}}}}"
            ] = produto.codigo

            substituicoes[
                f"{{{{PRODUTO{indice}}}}}"
            ] = produto.nome

            substituicoes[
                f"{{{{PRECO{indice}}}}}"
            ] = produto.preco

        return substituicoes

    def gerar(
        self,
        produtos: list[Produto],
    ) -> Path:
        documento = load(
            str(self.modelo.arquivo)
        )

        substituicoes = self._criar_substituicoes(
            produtos
        )

        self._substituir_marcadores(
            documento.text,
            substituicoes
        )

        arquivo_saida = gerar_nome_saida(
            self.modelo.nome,
            self.pasta_saida
        )

        documento.save(
            str(arquivo_saida)
        )

        return arquivo_saida