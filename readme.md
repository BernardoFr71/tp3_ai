Excelente\! Uma documentação de alta qualidade é crucial para qualquer projeto de software.

Vou criar um ficheiro `README.md` **completo e profissional** para o teu projeto "Parser", incluindo uma secção dedicada à nova *feature* de VP Chunking, que faz referência ao ficheiro `FEATURE_VP_CHUNKING.md` que criámos.

## 📄 Ficheiro `README.md` (Completo e Detalhado)

Cria um ficheiro chamado `README.md` na pasta principal do teu projeto e cola o conteúdo abaixo:

````markdown
# 🤖 CS50 AI: Projeto Parser (NP e VP Chunking)

## 🎯 Visão Geral

Este projeto, desenvolvido como parte do curso **CS50's Introduction to Artificial Intelligence with Python**, implementa um analisador sintático (parser) baseado em expressões regulares do NLTK (*RegexpParser*). O objetivo principal é realizar **Chunking** para identificar e extrair frases nominais (Noun Phrases - NP) e frases verbais (Verb Phrases - VP) em frases de texto.

O sistema utiliza a biblioteca `nltk` para pré-processamento (tokenização e POS tagging) e para a aplicação de gramáticas definidas por regras (*chunk grammars*).

---

## 🛠️ Tecnologias e Requisitos

* **Linguagem:** Python 3
* **Biblioteca Principal:** NLTK (Natural Language Toolkit)
* **Estrutura:** Utiliza scripts e argumentos de linha de comandos.

### Instalação

O projeto requer apenas a biblioteca `nltk`. Recomenda-se a utilização de um ambiente virtual (`venv`).

1.  **Criação do Ambiente Virtual (Opcional, mas Recomendado):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Linux/macOS
    .\.venv\Scripts\activate   # No Windows (PowerShell)
    ```

2.  **Instalação dos Requisitos:**
    Certifique-se de que o ficheiro `requirements.txt` contém a linha `nltk`.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Recursos do NLTK:** O script `parser.py` fará o download automático dos recursos necessários (`punkt` e `averaged_perceptron_tagger`) na primeira execução.

---

## 🚀 Como Executar

O programa deve ser executado a partir da linha de comandos, aceitando o caminho para o diretório que contém os ficheiros de sentenças de entrada (`1.txt` a `10.txt`).

### Estrutura de Pastas

O teu diretório deve ter a seguinte estrutura:

````

/tp3\_ai
├── parser.py
├── requirements.txt
└── sentences/
├── 1.txt
├── 2.txt
└── ... (até 10.txt)

````

### Comando

Execute o parser, passando o nome da pasta das sentenças como argumento:

```bash
python parser.py sentences
````

### Output Esperado

O programa irá iterar por cada ficheiro de sentença, mostrando:

1.  A frase original.
2.  Os tokens pré-processados.
3.  O **NP Chunking** (funcionalidade base do projeto).
4.  O **VP Chunking** e a **Identificação do Verbo Principal** (nova *feature*).

-----

## 🧠 Funcionalidades Implementadas

### 1\. Pré-processamento (`preprocess`)

Esta função prepara a frase de entrada para a análise sintática:

  * Converte a frase para minúsculas.
  * Tokeniza as palavras usando `nltk.word_tokenize`.
  * Remove todos os símbolos de pontuação.

### 2\. NP Chunking (`np_chunk`)

  * **Objetivo:** Identificar as Frases Nominais (NP).
  * **Gramática:** Aplica a regra padrão `NP: {<DT>?<JJ>*<NN.*>+}` para capturar o núcleo nominal (Nomes), precedido por Adjetivos e um Determinante opcional.

-----

## ✨ Nova Feature: VP Chunking e Head Verb Identification

Adicionámos uma nova funcionalidade que expande a capacidade de análise do parser para além das Frases Nominais. Esta *feature* é detalhada no seu próprio documento, mas um resumo das suas capacidades está abaixo.

### Componentes da Feature

| Função | Descrição |
| :--- | :--- |
| `vp_chunk` | Identifica as Frases Verbais (VP) usando uma gramática de chunk (`VP: {<VB.*>+<RB.?>*<RP>?<NN.*|DT>?}`). |
| `find_head_verb` | Analisa cada VP extraído e, através de heurísticas de POS-tagging, determina qual é o **Verbo Principal** (o núcleo semântico) do chunk. |

### Documentação Completa

Para uma análise aprofundada da lógica de implementação, gramática utilizada e regras de identificação do verbo principal, consulte o documento:

➡️ **[FEATURE\_VP\_CHUNKING.md](./FEATURE_VP_CHUNKING.md)**

-----

## ✒️ Licença

Este projeto é submetido sob a licença do CS50.

```
```