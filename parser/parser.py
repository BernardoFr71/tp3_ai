import nltk
import sys
import string
from nltk.tree import Tree

# Configuração inicial do NLTK
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except FileNotFoundError:
    pass

# -------------------------------------------------------------------------
# GRAMÁTICA CFG (Requisito Principal do CS50)
# Define a estrutura sintática das frases e o vocabulário.
# -------------------------------------------------------------------------

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N | NP PP | NP Conj NP
VP -> V | V NP | V NP PP | V PP | V Adv | Adv V | VP Conj VP | VP Adv | Adv V NP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

# -------------------------------------------------------------------------
# FUNÇÕES DO PARSER
# -------------------------------------------------------------------------

def preprocess(sentence):
    """
    Converte a frase para minúsculas e remove pontuação e palavras irrelevantes.
    """
    # Converter para minúsculas
    sentence = sentence.lower()
    
    # Tokenizar
    try:
        tokens = nltk.word_tokenize(sentence)
    except LookupError:
        tokens = sentence.split()

    # Filtrar pontuação e garantir que as palavras estão na gramática (opcional, mas seguro)
    # Mantemos apenas palavras que são alfanuméricas para remover pontuação solta
    filtered_tokens = [
        word for word in tokens 
        if word not in string.punctuation and any(c.isalnum() for c in word)
    ]

    return filtered_tokens

def np_chunk(tree):
    """
    Retorna uma lista de todos os 'noun phrase chunks' na árvore de sentenças.
    Um 'noun phrase chunk' é definido como uma subárvore NP que não contém
    outras subárvores NP dentro dela.
    """
    chunks = []
    
    # Percorrer todas as subárvores
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            # Verificar se esta NP contém outra NP dentro dela
            has_nested_np = False
            for child in subtree:
                if isinstance(child, Tree) and child.label() == "NP":
                    has_nested_np = True
                    break
            
            # Se não tiver NP aninhada, é um chunk válido
            if not has_nested_np:
                chunks.append(subtree)
                
    return chunks

# -------------------------------------------------------------------------
# FEATURE EXTRA: VP CHUNKING & HEAD VERB
# (Usa uma abordagem híbrida com RegexpParser para maior robustez na feature)
# -------------------------------------------------------------------------

def vp_chunk_feature(tokens):
    """
    [FEATURE EXTRA] Identifica VP Chunks usando POS-Tagging e RegexpParser.
    Retorna uma lista de tuplos: (VP String, Head Verb)
    """
    try:
        pos_tags = nltk.pos_tag(tokens)
    except LookupError:
        return []

    # Gramática específica para a Feature de VPs
    # Captura verbos, advérbios e partículas associadas
    vp_grammar = r"""
        VP: {<VB.*>+<RB.?>*<RP>?<DT|NN.*>?} 
    """
    
    cp = nltk.RegexpParser(vp_grammar)
    tree = cp.parse(pos_tags)
    
    results = []
    
    for subtree in tree.subtrees():
        if subtree.label() == "VP":
            # Reconstruir a frase do VP
            words = [w for w, t in subtree.leaves()]
            vp_str = " ".join(words)
            
            # Identificar Head Verb (Heurística: verbo não-auxiliar ou o último verbo)
            head_verb = None
            aux_verbs = ['be', 'is', 'are', 'was', 'were', 'have', 'had', 'do', 'did']
            
            # Procura o último verbo conjugado que não seja auxiliar comum
            leaves = subtree.leaves() # [(word, tag), ...]
            for word, tag in reversed(leaves):
                if tag.startswith('VB'):
                    if word not in aux_verbs:
                        head_verb = word
                        break
            
            # Fallback: se não achar (ex: "was"), pega o primeiro verbo que encontrar
            if not head_verb:
                for word, tag in leaves:
                    if tag.startswith('VB'):
                        head_verb = word
                        break
            
            results.append((vp_str, head_verb))
            
    return results

# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python parser.py directory")
    
    directory = sys.argv[1]
    
    print(f"CS50 AI Parser | Carregando sentenças de: {directory}")
    print("=" * 60)

    # Tenta ler arquivos de 1.txt a 10.txt (ajustar conforme necessidade)
    import os
    
    # Listar arquivos txt no diretório ordenadamente
    try:
        files = sorted([f for f in os.listdir(directory) if f.endswith(".txt")])
    except FileNotFoundError:
        sys.exit("Diretório não encontrado.")

    for filename in files:
        filepath = os.path.join(directory, filename)
        with open(filepath) as f:
            sentence = f.read().strip()
            
        print(f"\nFrase: {sentence}")
        
        # 1. Preprocessamento
        s = preprocess(sentence)
        if not s:
            continue
            
        # 2. Parsing CFG (Requisito CS50)
        try:
            trees = list(parser.parse(s))
        except ValueError as e:
            print(e)
            return

        if not trees:
            print("❌ Não foi possível fazer o parse da frase (Gramática insuficiente).")
        else:
            # Para o CS50, processamos a primeira árvore válida
            tree = trees[0]
            
            print("\n[ESTRUTURA SINTÁTICA - CFG]")
            tree.pretty_print()

            print("\n[REQ. 1: NP CHUNKS]")
            chunks = np_chunk(tree)
            if chunks:
                for chunk in chunks:
                    # 'flatten' converte a subárvore em texto simples novamente
                    print(f"  - {' '.join(chunk.flatten())}")
            else:
                print("  (Nenhum NP encontrado)")

            # 3. Nova Feature
            print("\n[REQ. 2: FEATURE EXTRA - VP ANALYSIS]")
            vp_data = vp_chunk_feature(s)
            if vp_data:
                for vp_str, head in vp_data:
                    print(f"  - VP: '{vp_str}' | Head Verb: '{head}'")
            else:
                print("  (Nenhum VP complexo encontrado)")
        
        print("-" * 60)

if __name__ == "__main__":
    main()