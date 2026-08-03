# LabelForge

> Ferramenta de linha de comando desenvolvida em Python para automatizar a geração de etiquetas de preço a partir de um orçamento em PDF.

## 📖 Sobre o projeto

O **LabelForge** foi criado por mim para uso no meu ambiente de trabalho, com o objetivo de eliminar tarefas repetitivas na produção de etiquetas e reduzir erros durante o preenchimento manual.

A aplicação lê um orçamento em PDF exportado pelo sistema **Farmax**, extrai automaticamente as informações dos produtos e gera um arquivo no formato **ODT**, preenchendo modelos de etiquetas prontos para impressão.

Embora tenha sido desenvolvido para atender uma necessidade real do meu trabalho, o projeto foi estruturado de forma modular, permitindo adaptações para outros modelos de etiquetas e documentos com formato semelhante.

> **Aviso:** Este é um projeto independente, desenvolvido por iniciativa própria. Não possui vínculo, aprovação ou suporte da empresa responsável pelo sistema Farmax.

---

# ✨ Funcionalidades

- Leitura automática de orçamentos em PDF.
- Extração de código, descrição e preço dos produtos.
- Preenchimento automático de modelos de etiquetas em ODT.
- Suporte a diferentes modelos de impressão.
- Geração automática do arquivo final.
- Organização dos arquivos de entrada e saída.

---

# 📋 Requisitos

- Python **3.10** ou superior

### Dependências

| Biblioteca | Finalidade |
|------------|------------|
| `pdfplumber` | Leitura do PDF |
| `odfpy` | Manipulação de documentos ODT |

---

# 📦 Instalação

## Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

# 📁 Estrutura do projeto

```
LabelForge/
│
├── input/          # PDFs de entrada
├── output/         # Arquivos gerados automaticamente
├── templates/      # Modelos de etiquetas (.odt)
│   ├── 10X1.odt
│   └── 24X1.odt
│
├── src/            # Código-fonte
├── requirements.txt
└── README.md
```

---

# 🚀 Como usar

## 1. Adicione o PDF

Coloque o orçamento em PDF dentro da pasta:

```
input/
```

Caso existam vários arquivos PDF, será utilizado o primeiro em ordem alfabética.

---

## 2. Execute o programa

```bash
python src/main.py
```

---

## 3. Escolha o modelo de etiqueta

```
1 → Modelo 10x1
2 → Modelo 24x1
```

---

## 4. Arquivo gerado

Após a execução, será criado um arquivo semelhante a:

```
output/
└── Etiquetas_10x1_03-08-2026_14-35-10.odt
```

---

# 📄 Formato esperado do PDF

Cada produto deve estar em uma única linha seguindo o padrão:

```
Código
Código de barras
Nome do produto
Quantidade
Preço unitário
Preço unitário
Preço total
```

### Exemplo

```
7 7891234560011 ARROZ TIO JOÃO 5 KG 2 29,90 29,90 59,80
```

---

# 🏷️ Marcadores dos modelos

Os arquivos ODT utilizam marcadores que são substituídos automaticamente.

| Marcador | Conteúdo |
|----------|----------|
| `{{CODIGO_N}}` | Código do produto |
| `{{PRODUTO_N}}` | Nome do produto |
| `{{PRECO_N}}` | Preço do produto |

Onde **N** representa a posição da etiqueta no modelo.

Exemplo:

```
{{CODIGO_1}}
{{PRODUTO_1}}
{{PRECO_1}}
```

---

# 📂 Modelos suportados

| Modelo | Descrição |
|---------|-----------|
| **10x1** | 10 etiquetas por página |
| **24x1** | 24 etiquetas por página |

Novos modelos podem ser adicionados à pasta `templates/`.

---

## 💡 Motivação

Durante minha rotina de trabalho, percebi que a criação manual de etiquetas consumia tempo e estava sujeita a erros de digitação. Para resolver esse problema, desenvolvi o **LabelForge**, uma ferramenta capaz de transformar automaticamente um orçamento exportado pelo sistema **Farmax** em um documento de etiquetas pronto para impressão.

Além de otimizar o processo, o projeto também serviu como uma oportunidade para aplicar conhecimentos de Python, manipulação de PDFs, automação de documentos e desenvolvimento de ferramentas voltadas para problemas reais do dia a dia.

---

# ⚠️ Limitações

- O PDF deve seguir o formato esperado pelo programa.
- Apenas arquivos PDF são aceitos como entrada.
- Os modelos devem estar no formato ODT.
- Alterações no layout do PDF de origem podem exigir ajustes na lógica de extração.

---

# 🛠️ Tecnologias utilizadas

- Python 3
- pdfplumber
- odfpy

---

# 📄 Licença

Este projeto é disponibilizado para fins de estudo e uso pessoal. Adapte-o conforme sua necessidade, respeitando as licenças das bibliotecas utilizadas.