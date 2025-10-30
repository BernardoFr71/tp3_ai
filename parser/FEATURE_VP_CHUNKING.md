# FEATURE: VP CHUNKING AND HEAD VERB IDENTIFICATION

## 🌿 Branch: `feature/vp-chunking`

## 📝 Descrição da Funcionalidade

Esta funcionalidade estende o parser de base (focado em NP Chunking) para incluir a identificação de Verb Phrases (VPs) e o seu núcleo semântico, o Verbo Principal (Head Verb).

A **Análise de VP** e a **Identificação do Head Verb** são passos cruciais para a extração de relações e a análise de dependências sintáticas, fornecendo uma camada de informação semântica mais rica para o sistema.

## 🛠️ Alterações Implementadas em `parser.py`

### 1. VP Chunking (`vp_chunk`)

* **Objetivo:** Identificar o conjunto de palavras que funcionam como o predicado da frase (verbo e modificadores imediatos).
* **Método:** Utiliza `nltk.RegexpParser` com uma gramática específica:
    * **Gramática:** `VP: {<VB.*>+<RB.?>*<RP>?<NN.*|DT>?}`
    * **Componentes:** Procura por **um ou mais Verbos** (`<VB.*>+`), seguidos opcionalmente por Advérbios (`<RB.?>*`), Partículas (`<RP>?`), e, heuristicamente, um Nome ou Determinante que pode iniciar o objeto.

### 2. Identificação do Verbo Principal (`find_head_verb`)

* **Objetivo:** Determinar a palavra que carrega o significado principal da ação dentro do VP.
* **Lógica Heurística:**
    * **Prioridade:** Procura o **último Verbo conjugado** dentro do VP (e.g., VBD, VBZ) que **não** seja um verbo auxiliar comum (como 'be', 'have', 'do' ou modais).
    * Esta regra garante que o verbo principal é identificado corretamente, mesmo na presença de auxiliares (ex: em "is walking", o *head verb* é "walking").

### 3. Integração na `main`

A função `main` foi atualizada para processar as sentenças e agora apresenta **três níveis de análise**:

1.  **[FUNCIONALIDADE ORIGINAL] NP Chunks:** Os Noun Phrases.
2.  **[NOVA FEATURE: VP CHUNKING] VP Chunks:** Os Verb Phrases identificados pela nova gramática.
3.  **[NOVA FEATURE: HEAD VERB] Verbo Principal:** O núcleo da ação de cada VP.

## 🚀 Como Testar

Execute o script diretamente a partir da linha de comandos:

```bash
python parser.py sentences