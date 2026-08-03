# LabelForge

> Ferramenta de linha de comando desenvolvida em Python para automatizar a geração de etiquetas de preço a partir de um orçamento em PDF.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![PDF](https://img.shields.io/badge/PDF-processing-red?logo=adobeacrobatreader&logoColor=white)
![ODT](https://img.shields.io/badge/ODT-generation-orange)
![Status](https://img.shields.io/badge/status-concluído-success)

## 📖 Sobre o projeto

O **LabelForge** foi criado por mim para uso no meu ambiente de trabalho, com o objetivo de reduzir tarefas repetitivas no processo de produção de etiquetas e diminuir erros durante o preenchimento manual.

A aplicação lê um orçamento em PDF gerado pelo sistema de gestão **Farmax**, extrai automaticamente as informações dos produtos e gera um arquivo no formato **ODT**, preenchendo modelos de etiquetas prontos para impressão.

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

- Python **3.10** ou superior.

### Dependências

As bibliotecas utilizadas estão listadas no arquivo `requirements.txt`.

| Biblioteca | Finalidade |
|------------|------------|
| `pdfplumber` | Leitura e extração de informações do PDF |
| `odfpy` | Manipulação e geração de documentos ODT |

---

# 📦 Instalação

## Windows

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

# 📁 Estrutura do Projeto

```text
LabelForge/
│
├── input/              # PDFs de entrada
├── output/             # Arquivos gerados automaticamente
├── templates/          # Modelos de etiquetas (.odt)
│   ├── 10x1.odt
│   └── 24x1.odt
│
├── src/                # Código-fonte
│   ├── config.py
│   ├── generator.py
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   └── utils.py
│
├── requirements.txt
└── README.md
```

## Responsabilidade dos módulos

| Arquivo | Responsabilidade |
|---------|------------------|
| `main.py` | Ponto de entrada da aplicação. Coordena todo o fluxo de execução, desde a localização do PDF e escolha do modelo até a geração do arquivo final de etiquetas. |
| `config.py` | Centraliza as configurações do projeto, incluindo os caminhos das pastas (`input`, `output` e `templates`) e a definição dos modelos de etiquetas disponíveis. |
| `parser.py` | Implementa a classe `PDFParser`, responsável por ler o orçamento em PDF, corrigir inconsistências na extração de texto, identificar as linhas de produtos e convertê-las em objetos `Produto`. |
| `generator.py` | Implementa a classe `ODTGenerator`, responsável por carregar um modelo ODT, substituir os marcadores pelos dados dos produtos e gerar o arquivo final de etiquetas. |
| `models.py` | Define as classes de domínio da aplicação (`Produto` e `ModeloEtiqueta`), utilizadas para representar de forma estruturada os dados processados entre os módulos. |
| `utils.py` | Reúne funções auxiliares reutilizadas pela aplicação, como validação de arquivos, geração de nomes para os arquivos de saída e utilidades de apoio à interface de linha de comando. |

> **Arquitetura:** O projeto foi organizado em módulos com responsabilidades bem definidas, seguindo o princípio da responsabilidade única (*Single Responsibility Principle – SRP*). Essa organização facilita a manutenção, a reutilização de código e futuras expansões, como suporte a novos formatos de PDF, novos modelos de etiquetas ou diferentes interfaces de usuário.

---

# 🚀 Como usar

## 1. Adicione o PDF

Coloque o orçamento em PDF dentro da pasta:

```text
input/
```

Caso exista mais de um arquivo PDF, o primeiro encontrado em ordem alfabética será utilizado.

---

## 2. Execute o programa

Na raiz do projeto:

```bash
python src/main.py
```

---

## 3. Escolha o modelo de etiqueta

```text
1 → Modelo 10x1
2 → Modelo 24x1
```

---

## 4. Arquivo gerado

Após a execução, será criado um arquivo semelhante a:

```text
output/
└── Etiquetas_10x1_03-08-2026_14-35-10.odt
```

---

# 📄 Formato esperado do PDF

O programa espera encontrar produtos em linhas contendo:

```text
Código interno
Código de barras
Nome do produto
Quantidade
Preço unitário
Preço unitário
Preço total
```

### Exemplo

```text
7 7891234560011 ARROZ TIO JOÃO 5 KG 2 29,90 29,90 59,80
```

O código de barras é utilizado como referência para identificação da estrutura da linha durante a extração dos dados.

---

# 🏷️ Marcadores dos modelos

Os arquivos ODT utilizam marcadores que são substituídos automaticamente pelos dados dos produtos.

| Marcador | Conteúdo |
|----------|----------|
| `{{CODIGO1}}` | Código do produto |
| `{{PRODUTO1}}` | Nome do produto |
| `{{PRECO1}}` | Preço do produto |

O número representa a posição da etiqueta no modelo.

Exemplo para a primeira etiqueta:

```text
{{CODIGO1}}
{{PRODUTO1}}
{{PRECO1}}
```

Exemplo para a segunda etiqueta:

```text
{{CODIGO2}}
{{PRODUTO2}}
{{PRECO2}}
```

---

# 📂 Modelos suportados

| Modelo | Descrição |
|---------|-----------|
| **10x1** | 10 etiquetas por página |
| **24x1** | 24 etiquetas por página |

Novos modelos podem ser adicionados à pasta:

```text
templates/
```

---

# 💡 Motivação

Durante minha rotina de trabalho, percebi que a criação manual de etiquetas consumia tempo e estava sujeita a erros de digitação.

Para resolver esse problema, desenvolvi o **LabelForge**, uma ferramenta capaz de transformar automaticamente um orçamento exportado pelo sistema **Farmax** em um documento de etiquetas pronto para impressão.

Além de otimizar o processo, o projeto também serviu como uma oportunidade para aplicar conhecimentos em:

- Python;
- Manipulação de PDFs;
- Automação de documentos;
- Estruturação de projetos;
- Desenvolvimento de ferramentas para problemas reais do dia a dia.

---

# ⚠️ Limitações

- O PDF deve seguir o formato esperado pelo programa.
- Apenas arquivos PDF são aceitos como entrada.
- Os modelos devem estar no formato ODT.
- Alterações no layout do PDF de origem podem exigir ajustes na lógica de extração.

---

# 🛠️ Tecnologias utilizadas

- Python 3
- `pdfplumber`
- `odfpy`

---

# 📄 Licença

Este projeto é disponibilizado para fins educacionais e demonstração de desenvolvimento.

Respeite as licenças das bibliotecas utilizadas e adapte o projeto conforme sua necessidade.