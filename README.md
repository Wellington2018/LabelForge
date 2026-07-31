# LabelForge

Ferramenta de linha de comando que lê um orçamento em PDF, extrai os produtos encontrados e gera um arquivo ODT com etiquetas prontas para impressão, substituindo os dados nos modelos pré-configurados.

# Requisitos

- Python 3.10 ou superior
- Dependências listadas em `requirements.txt`:
- `pdfplumber` — leitura do PDF
- `odfpy` — manipulação do documento ODT

# Instalação

Windows

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Estrutura de pastas

     LabelForge/
     ├── input/       # Coloque aqui o PDF do orçamento
     ├── output/      # Etiquetas geradas (criada automaticamente)
     ├── templates/   # Modelos ODT (10X1.odt e 24X1.odt)
     └── src/         # Código-fonte

# Como usar

1. Crie a pasta `input/` e coloque dentro dela o PDF do orçamento. Caso haja mais de um PDF, o primeiro (em ordem alfabética) é utilizado.

2. Execute o programa a partir da raiz do projeto:

bash
python src/main.py

3. Escolha o modelo de etiqueta:

- `1` — modelo **10x1** (10 etiquetas por página)
- `2` — modelo **24x1** (24 etiquetas por página)

4. O programa lista os produtos encontrados e gera o arquivo em `output/Etiquetas_<modelo>_<data>_<hora>.odt`.

# Formato esperado do PDF

Cada produto deve estar em uma única linha, contendo, nesta ordem:

     código  código de barras  nome  quantidade  preço  preço  preço

Exemplo:


     7 7891234560011 ARROZ TIO JOÃO 5 KG 2 29,90 29,90 59,80

# Marcadores do modelo

Os arquivos ODT em `templates/` usam marcadores que são substituídos pelos dados de cada produto:

     | Marcador        | Substituído por    |
     |-----------------|--------------------|
     | `{{CODIGO_N}}`  | Código do produto  |
     | `{{PRODUTO_N}}` | Nome do produto    |
     | `{{PRECO_N}}`   | Preço do produto   |
                                                                                               