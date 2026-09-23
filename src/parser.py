from __future__ import annotations

import re
from pathlib import Path
from typing import List

import pdfplumber

from models import Produto


class PDFParser:

    def __init__(self, pdf_path: Path):
        self.pdf_path = Path(pdf_path)

    def _ler_pdf(self) -> str:

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


        linha = re.sub(
            r"^(\d+)\s+(\d{8,13})([A-ZÁÉÍÓÚÃÕÇ])",
            r"\1 \2 \3",
            linha,
        )


        linha = re.sub(
            r"([A-ZÁÉÍÓÚÃÕÇ])(\d+)\s+(\d+,\d{2})\s+\d+,\d{2}\s+\d+,\d{2}$",
            r"\1 \2 \3 0,00 0,00",
            linha,
        )

        return linha

    def _linha_eh_produto(self, linha: str) -> bool:

        return bool(
            re.match(
                r"^\d+\s+\d{8,13}",
                linha,
            )
        )

    def _extrair_produto(self, linha: str) -> Produto | None:

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

    def extrair_produtos(self) -> List[Produto]:

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
