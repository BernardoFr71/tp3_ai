import nltk
import sys
import string
from typing import List, Tuple

# Download necessário do NLTK
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except Exception as e:
    print(f"Aviso: Não foi possível baixar recursos do NLTK. {e}")
    print("O programa pode falhar se os recursos não estiverem disponíveis.")

def preprocess(sentence: str) -> List[str]:
    """
    Converte a frase para minúsculas, tokeniza e remove pontuação.
    """
    sentence = sentence.lower()
    
    try:
        tokens = nltk.word_tokenize(sentence)
    except:
        tokens = sentence.split()
    
    filtered_tokens = [token for token in tokens if token not in string.punctuation]
    
    return filtered_tokens

def np_chunk(tokens: List[str]) -> List[str]:
    """
    Extrai Noun Phrases (NPs) dos tokens usando o NLTK RegexpParser (Chunking).
    """
    try:
        pos_tags = nltk.pos_tag(tokens)
    except:
        pos_tags = [(token, 'NN') for token in tokens]

    # Gramática para NP: Determinante opcional, Adjetivos, Nomes
    grammar = "NP: {<DT>?<JJ>*<NN.*>+}"
    
    chunk_parser = nltk.RegexpParser(grammar)
    tree = chunk_parser.parse(pos_tags)
    
    np_chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            chunk_words = [word for word, tag in subtree.leaves()]
            np_chunks.append(" ".join(chunk_words))
    
    # Remover duplicados enquanto preserva a ordem
    seen = set()
    unique_chunks = []
    for chunk in np_chunks:
        if chunk not in seen:
            seen.add(chunk)
            unique_chunks.append(chunk)
    
    return unique_chunks

# -------------------- NOVA FEATURE: VP CHUNKING --------------------

def vp_chunk(tokens: List[str]) -> List[str]:
    """
    FEATURE: Extrai Verb Phrases (VPs) dos tokens usando o NLTK RegexpParser (Chunking).
    """
    try:
        pos_tags = nltk.pos_tag(tokens)
    except:
        pos_tags = [(token, 'NN') for token in tokens]

    # Gramática para VP: Um ou mais verbos (VB.*) seguido por Advérbios, Partículas, Nomes/Determinantes opcionais.
    # Esta regra captura a maioria dos núcleos verbais e seus modificadores imediatos.
    grammar = "VP: {<VB.*>+<RB.?>*<RP>?<NN.*|DT>?}"
    
    chunk_parser = nltk.RegexpParser(grammar)
    tree = chunk_parser.parse(pos_tags)
    
    vp_chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == 'VP':
            chunk_words = [word for word, tag in subtree.leaves()]
            vp_chunks.append(" ".join(chunk_words))
    
    # Remover duplicados
    seen = set()
    unique_chunks = []
    for chunk in vp_chunks:
        if chunk not in seen:
            seen.add(chunk)
            unique_chunks.append(chunk)
    
    return unique_chunks

def find_head_verb(vp_chunk: str, tokens: List[str]) -> str:
    """
    FEATURE: Identifica o "Head Verb" (verbo principal) dentro de um VP chunk.
    Usa regras heurísticas baseadas em POS tagging.
    """
    vp_tokens = nltk.word_tokenize(vp_chunk.lower())
    
    try:
        vp_pos_tags = nltk.pos_tag(vp_tokens)
    except:
        return f"Erro ao etiquetar: {vp_chunk}"

    auxiliary_verbs = ['be', 'is', 'are', 'was', 'were', 'am', 'have', 'has', 'had', 'do', 'does', 'did', 'can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would']

    # 1. Procura pelo último verbo conjugado (VB, VBD, VBZ) que não seja auxiliar.
    for word, tag in reversed(vp_pos_tags):
        if tag.startswith('VB') and word not in auxiliary_verbs:
            return word
    
    # 2. Se falhar, devolve o primeiro verbo que encontrar (pode ser auxiliar ou infinitivo).
    for word, tag in vp_pos_tags:
        if tag.startswith('VB'):
            return word

    return "Não encontrado"

# ------------------ FIM DA NOVA FEATURE ------------------


def main():
    """
    Main function to run the parser on sentences from files,
    agora incluindo VP Chunking.
    """
    if len(sys.argv) != 2:
        print("Uso: python parser.py <sentences_directory>")
        sys.exit(1)
    
    sentences_dir = sys.argv[1]
    
    # Nome da Feature Branch na execução
    print("CS50 AI Parser Project - NP/VP Chunking (Feature: VP_CHUNKING)")
    print("=" * 70)
    
    # Process each sentence file
    for i in range(1, 11):
        filename = f"{sentences_dir}/{i}.txt"
        try:
            with open(filename, 'r') as file:
                sentence = file.read().strip()
                
            print(f"\nSentence {i}: {sentence}")
            print("-" * 40)
            
            # Preprocess
            tokens = preprocess(sentence)
            print(f"Tokens: {tokens}")
            
            # 1. NP Chunking (Funcionalidade Original)
            np_chunks = np_chunk(tokens)
            print(f"\n[FUNCIONALIDADE ORIGINAL] NP Chunks: {np_chunks}")
            
            # 2. VP Chunking (NOVA FEATURE)
            vp_chunks = vp_chunk(tokens)
            print(f"\n[NOVA FEATURE: VP CHUNKING] VP Chunks: {vp_chunks}")
            
            # 3. Head Verb Identification (NOVA FEATURE)
            print("[NOVA FEATURE: HEAD VERB]")
            if vp_chunks:
                for chunk in vp_chunks:
                    head_verb = find_head_verb(chunk, tokens)
                    print(f"  -> VP: '{chunk}' | Verbo Principal: '{head_verb}'")
            else:
                print("  -> Nenhum VP encontrado.")
                
        except FileNotFoundError:
            print(f"ERRO: Ficheiro {filename} não encontrado. Certifique-se de que a pasta '{sentences_dir}' existe.")
        except Exception as e:
            print(f"ERRO ao processar {filename}: {e}")

if __name__ == "__main__":
    main()