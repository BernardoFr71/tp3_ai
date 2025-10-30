import nltk
import sys
import string
from nltk import CFG
from nltk.tree import Tree

# Download necessário do NLTK
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    print("Aviso: Alguns recursos do NLTK podem não estar disponíveis")

def preprocess(sentence):
    """
    Convert sentence to lowercase and tokenize words
    Remove punctuation marks
    """
    # Convert to lowercase
    sentence = sentence.lower()
    
    # Tokenize the sentence
    try:
        tokens = nltk.word_tokenize(sentence)
    except:
        # Fallback simple tokenization
        tokens = sentence.split()
    
    # Remove punctuation tokens
    filtered_tokens = [token for token in tokens if token not in string.punctuation]
    
    return filtered_tokens

def custom_grammar_parse(tokens):
    """
    Parse tokens using a custom CFG grammar
    Return the first valid parse tree or None if no parse found
    """
    # Gramática CFG expandida para cobrir mais construções
    grammar = CFG.fromstring("""
        S -> NP VP | S Conj S | VP
        NP -> PropN | Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N | NP PP | N
        VP -> V | V NP | V PP | V NP PP | VP PP | V Adv | VP Conj VP | V Adv NP | V Particle
        PP -> P NP
        Particle -> 'down'
        
        Det -> 'the' | 'a' | 'an' | 'my' | 'your' | 'his' | 'her' | 'our' | 'their'
        N -> 'holmes' | 'pipe' | 'day' | 'companion' | 'smile' | 'word' | 'door' | 'walk' | 'home' | 'mess' | 'paint' | 'palm' | 'hand' | 'thursday' | 'armchair' | 'himself'
        Adj -> 'red' | 'enigmatical' | 'country' | 'dreadful' | 'little' | 'moist'
        V -> 'sat' | 'lit' | 'arrived' | 'chuckled' | 'smiled' | 'said' | 'were' | 'came' | 'had' | 'down'
        P -> 'in' | 'on' | 'at' | 'with' | 'to' | 'from' | 'before' | 'until' | 'of'
        PropN -> 'holmes' | 'we' | 'i' | 'he' | 'she' | 'himself'
        Adv -> 'quickly' | 'slowly' | 'yesterday' | 'never' | 'here'
        Conj -> 'and' | 'or' | 'but'
    """)
    
    # Create parser
    parser = nltk.ChartParser(grammar)
    
    try:
        # Get all possible parse trees
        trees = list(parser.parse(tokens))
        if trees:
            return trees[0]  # Return first valid parse
        else:
            return None
    except Exception as e:
        return None

def np_chunk(tokens):
    """
    Extract noun phrases from tokens using improved rule-based chunking
    """
    # Perform POS tagging for better accuracy
    try:
        pos_tags = nltk.pos_tag(tokens)
    except:
        pos_tags = [(token, 'UNK') for token in tokens]
    
    np_chunks = []
    i = 0
    n = len(tokens)
    
    while i < n:
        current_chunk = []
        
        # Pattern 1: Personal pronouns (I, we, he, she, etc.)
        if tokens[i] in ['i', 'we', 'he', 'she', 'they', 'you']:
            np_chunks.append(tokens[i])
            i += 1
            continue
            
        # Pattern 2: Determiner + Adjectives + Noun
        if tokens[i] in ['the', 'a', 'an', 'my', 'your', 'his', 'her', 'our', 'their']:
            current_chunk.append(tokens[i])
            i += 1
            
            # Collect all consecutive adjectives
            while i < n and tokens[i] in ['red', 'enigmatical', 'country', 'dreadful', 'little', 'moist', 'big', 'small']:
                current_chunk.append(tokens[i])
                i += 1
            
            # Add the noun if present
            if i < n and tokens[i] in ['holmes', 'pipe', 'day', 'companion', 'smile', 'word', 
                                     'door', 'walk', 'home', 'mess', 'paint', 'palm', 'hand', 
                                     'thursday', 'armchair', 'himself']:
                current_chunk.append(tokens[i])
                i += 1
                
            if len(current_chunk) > 1:  # At least determiner + noun
                np_chunks.append(' '.join(current_chunk))
            continue
            
        # Pattern 3: Standalone nouns
        if tokens[i] in ['holmes', 'pipe', 'day', 'companion', 'smile', 'word', 
                       'door', 'walk', 'home', 'mess', 'paint', 'palm', 'hand', 
                       'thursday', 'armchair', 'himself']:
            np_chunks.append(tokens[i])
            
        i += 1
    
    # Remove duplicates while preserving order
    seen = set()
    unique_chunks = []
    for chunk in np_chunks:
        if chunk not in seen:
            seen.add(chunk)
            unique_chunks.append(chunk)
    
    return unique_chunks

def main():
    """
    Main function to run the parser on sentences from files
    """
    if len(sys.argv) != 2:
        print("Usage: python parser.py <sentences_directory>")
        sys.exit(1)
    
    sentences_dir = sys.argv[1]
    
    print("CS50 AI Parser Project - NP Chunking with CFG")
    print("=" * 60)
    
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
            
            # CFG Parsing
            cfg_tree = custom_grammar_parse(tokens)
            if cfg_tree:
                print("\nCFG Parse Tree:")
                cfg_tree.pretty_print()
            else:
                print("\nCFG Parse Tree: No valid parse found")
            
            # NP Chunking
            chunks = np_chunk(tokens)
            print(f"\nNP Chunks: {chunks}")
                
        except FileNotFoundError:
            print(f"File {filename} not found")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()