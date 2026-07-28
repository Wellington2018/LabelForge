"""
parser.py

Responsável pela leitura do orçamento em PDF e pela extração
dos produtos encontrados.

Autor: Wellington Oliveira
Projeto: LabelForge
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

import pdfplumber

from models import Produto


class PDFParser:
    """
    Faz a leitura de um orçamento em PDF e extrai os produtos.

    Exemplo:

        parser = PDFParser("orcamento.pdf")
        produtos = parser.extrair_produtos()
    """

    def __init__(self, pdf_path: Path):
        self.pdf_path = Path(pdf_path)

    # ---------------------------------------------------------
    # MÉTODOS PRIVADOS
    # ---------------------------------------------------------

    def _ler_pdf(self) -> str:
        """
        Lê todas as páginas do PDF e retorna o texto completo.
        """

        texto = ""

        try:
            with pdfplumber.open(self.pdf_path) as pdf:

                for pagina in pdf.pages:

                    conteudo = pagina.extract_text()

                    if conteudo:
                        texto += conteudo + "\n"

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo não encontrado:\n{self.pdf_path.resolve()}"
            )

        except Exception as erro:
            raise RuntimeError(
                f"Erro ao abrir PDF:\n{erro}"
            ) from erro

        return texto

    def _corrigir_linha(self, linha: str) -> str:
        """
        Corrige pequenos problemas de OCR ou de extração
        encontrados no PDF.
        """

        # Quando o nome fica colado ao código de barras.

        linha = re.sub(
            r"^(\d+)\s+(\d{8,13})([A-ZÁÉÍÓÚÃÕÇ])",
            r"\1 \2 \3",
            linha,
        )

        # Quando uma palavra cola no número.

        linha = re.sub(
            r"([A-ZÁÉÍÓÚÃÕÇ])(\d+)\s+(\d+,\d{2})\s+\d+,\d{2}\s+\d+,\d{2}$",
            r"\1 \2 \3 0,00 0,00",
            linha,
        )

        return linha

    def _linha_eh_produto(self, linha: str) -> bool:
        """
        Verifica se a linha parece representar um produto.
        """

        return bool(
            re.match(
                r"^\d+\s+\d{8,13}",
                linha,
            )
        )

    def _extrair_produto(self, linha: str) -> Produto | None:
        """
        Extrai um único produto da linha.
        """

        padrao = re.compile(
            r"""
            ^
            (\d+)                   # Código interno
            \s+
            \d{8,13}                # Código de barras
            \s+
            (.+?)                   # Nome
            \s+
            (\d+)                   # Quantidade
            \s+
            (\d+,\d{2})             # Preço
            \s+
            \d+,\d{2}
            \s+
            \d+,\d{2}
            $
            """,
            re.VERBOSE,
        )

        resultado = padrao.match(linha)

        if resultado is None:
            return None

        codigo = resultado.group(1)
        nome = resultado.group(2).strip()
        preco = f"R$ {resultado.group(4)}"

        return Produto(
            codigo=codigo,
            nome=nome,
            preco=preco,
        )

    # ---------------------------------------------------------
    # MÉTODO PÚBLICO
    # ---------------------------------------------------------

    def extrair_produtos(self) -> List[Produto]:
        """
        Extrai todos os produtos encontrados no PDF.
        """

        texto = self._ler_pdf()

        produtos: List[Produto] = []

        for linha in texto.splitlines():

            linha = linha.strip()

            if not linha:
                continue

            if not self._linha_eh_produto(linha):
                continue

            linha = self._corrigir_linha(linha)

            produto = self._extrair_produto(linha)

            if produto:
                produtos.append(produto)

        return produtos
