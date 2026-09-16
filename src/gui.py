import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog

from config import INPUT_DIR, OUTPUT_DIR, MODELOS
from parser import PDFParser
from generator import ODTGenerator
from models import ModeloEtiqueta


ultimo_arquivo_gerado = None


def selecionar_pdf():
    arquivo = filedialog.askopenfilename(
        title="Selecionar orçamento",
        initialdir=INPUT_DIR,
        filetypes=[
            ("Arquivos PDF", "*.pdf"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if arquivo:
        campo_pdf.delete(0, tk.END)
        campo_pdf.insert(0, arquivo)
        atualizar_status("PDF selecionado.", sucesso=False)


def gerar_etiquetas():
    global ultimo_arquivo_gerado

    caminho_pdf = campo_pdf.get().strip()
    modelo_selecionado = modelo.get()

    if not caminho_pdf:
        atualizar_status(
            "Selecione um arquivo PDF.",
            sucesso=False
        )
        return

    caminho_pdf = Path(caminho_pdf)

    if not caminho_pdf.exists():
        atualizar_status(
            "O arquivo PDF não foi encontrado.",
            sucesso=False
        )
        return

    if caminho_pdf.suffix.lower() != ".pdf":
        atualizar_status(
            "O arquivo selecionado não é um PDF.",
            sucesso=False
        )
        return

    if not modelo_selecionado:
        atualizar_status(
            "Selecione um modelo de etiqueta.",
            sucesso=False
        )
        return

    configuracao_modelo = None

    for dados in MODELOS.values():
        if dados["nome"] == modelo_selecionado:
            configuracao_modelo = dados
            break

    if configuracao_modelo is None:
        atualizar_status(
            "Modelo de etiqueta inválido.",
            sucesso=False
        )
        return

    arquivo_template = configuracao_modelo["arquivo"]

    if not arquivo_template.exists():
        atualizar_status(
            f"Template não encontrado: {arquivo_template.name}",
            sucesso=False
        )
        return

    modelo_etiqueta = ModeloEtiqueta(
        nome=configuracao_modelo["nome"],
        arquivo=configuracao_modelo["arquivo"],
        limite=configuracao_modelo["limite"]
    )

    try:
        atualizar_status(
            "Lendo orçamento...",
            sucesso=False
        )

        janela.update_idletasks()

        parser = PDFParser(caminho_pdf)

        produtos = parser.extrair_produtos()

        if not produtos:
            atualizar_status(
                "Nenhum produto foi encontrado no PDF.",
                sucesso=False
            )
            return

        atualizar_status(
            f"{len(produtos)} produto(s) encontrado(s).",
            sucesso=False
        )

        janela.update_idletasks()

        gerador = ODTGenerator(
            modelo=modelo_etiqueta,
            pasta_saida=OUTPUT_DIR
        )

        arquivo_gerado = gerador.gerar(produtos)

        ultimo_arquivo_gerado = Path(arquivo_gerado)

        atualizar_status(
            "Geração concluída",
            sucesso=True
        )

        botao_abrir.config(
            state="normal"
        )

        botao_pasta.config(
            state="normal"
        )

    except Exception as erro:
        ultimo_arquivo_gerado = None

        botao_abrir.config(
            state="disabled"
        )

        botao_pasta.config(
            state="disabled"
        )

        atualizar_status(
            f"Erro: {erro}",
            sucesso=False
        )


def abrir_arquivo():
    if ultimo_arquivo_gerado is None:
        return

    if not ultimo_arquivo_gerado.exists():
        atualizar_status(
            "O arquivo gerado não foi encontrado.",
            sucesso=False
        )
        return

    os.startfile(
        ultimo_arquivo_gerado.resolve()
    )


def abrir_pasta():
    if ultimo_arquivo_gerado is None:
        return

    pasta = ultimo_arquivo_gerado.parent

    if pasta.exists():
        os.startfile(
            pasta.resolve()
        )


def atualizar_status(mensagem, sucesso=False):
    if sucesso:
        status_label.config(
            text="✓ " + mensagem
        )
    else:
        status_label.config(
            text=mensagem
        )


janela = tk.Tk()

janela.title("LabelForge")
janela.geometry("450x600")
janela.minsize(400, 500)

janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

conteudo = ttk.Frame(
    janela,
    padding=20
)

conteudo.grid(
    row=0,
    column=0,
    sticky="nsew"
)

conteudo.columnconfigure(0, weight=1)
conteudo.rowconfigure(2, weight=1)

titulo = ttk.Label(
    conteudo,
    text="LabelForge",
    font=("Arial", 24, "bold")
)

titulo.grid(
    row=0,
    column=0,
    sticky="n",
    pady=(10, 5)
)

subtitulo = ttk.Label(
    conteudo,
    text="Gerador de etiquetas de preço"
)

subtitulo.grid(
    row=1,
    column=0,
    sticky="n",
    pady=(0, 25)
)

frame = ttk.Frame(
    conteudo
)

frame.grid(
    row=2,
    column=0,
    sticky="nsew"
)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)

ttk.Label(
    frame,
    text="Arquivo PDF:"
).grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(0, 10)
)

campo_pdf = ttk.Entry(
    frame
)

campo_pdf.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=(0, 10)
)

botao_pdf = ttk.Button(
    frame,
    text="...",
    command=selecionar_pdf,
    width=5
)

botao_pdf.grid(
    row=1,
    column=1,
    sticky="ew"
)

ttk.Label(
    frame,
    text="Modelo:"
).grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(30, 10)
)

modelo = tk.StringVar(
    value="24x1"
)

frame_modelos = ttk.Frame(
    frame
)

frame_modelos.grid(
    row=3,
    column=0,
    columnspan=2,
    sticky="ew"
)

frame_modelos.columnconfigure(0, weight=1)
frame_modelos.columnconfigure(1, weight=1)
frame_modelos.columnconfigure(2, weight=1)

frame_modelos_interno = ttk.Frame(
    frame_modelos
)

frame_modelos_interno.grid(
    row=0,
    column=0,
    columnspan=3
)

radio_10x1 = ttk.Radiobutton(
    frame_modelos_interno,
    text="10x1",
    variable=modelo,
    value="10x1"
)

radio_10x1.grid(
    row=0,
    column=0,
    padx=15,
    pady=3
)

radio_24x1 = ttk.Radiobutton(
    frame_modelos_interno,
    text="24x1",
    variable=modelo,
    value="24x1"
)

radio_24x1.grid(
    row=0,
    column=1,
    padx=15,
    pady=3
)

radio_a4 = ttk.Radiobutton(
    frame_modelos_interno,
    text="A4",
    variable=modelo,
    value="A4"
)

radio_a4.grid(
    row=0,
    column=2,
    padx=15,
    pady=3
)

radio_a5 = ttk.Radiobutton(
    frame_modelos_interno,
    text="A5",
    variable=modelo,
    value="A5"
)

radio_a5.grid(
    row=0,
    column=3,
    padx=15,
    pady=3
)

botao_gerar = ttk.Button(
    frame,
    text="GERAR ETIQUETAS",
    command=gerar_etiquetas
)

botao_gerar.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=15
)

status_label = ttk.Label(
    frame,
    text="Aguardando geração..."
)

status_label.grid(
    row=5,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(0, 25)
)

frame_acoes = ttk.Frame(
    frame
)

frame_acoes.grid(
    row=6,
    column=0,
    columnspan=2,
    sticky="ew"
)

frame_acoes.columnconfigure(0, weight=1)
frame_acoes.columnconfigure(1, weight=1)

botao_abrir = ttk.Button(
    frame_acoes,
    text="ABRIR ARQUIVO",
    command=abrir_arquivo,
    state="disabled"
)

botao_abrir.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=(0, 5)
)

botao_pasta = ttk.Button(
    frame_acoes,
    text="ABRIR PASTA",
    command=abrir_pasta,
    state="disabled"
)

botao_pasta.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=(5, 0)
)

rodape = ttk.Label(
    conteudo,
    text="Desenvolvido por Wellington Oliveira",
    font=("Arial", 8)
)

rodape.grid(
    row=3,
    column=0,
    sticky="s",
    pady=(20, 5)
)

janela.mainloop()
