import nltk 
import random
from nltk.corpus import wordnet

def synonym_replacement(text, n=3):
    # Replace words in the text with their synonyms using NLTK or WordNet.
    with open(text, 'r') as f:
        lines = f.readlines()
    cleaned_lines = []
    for line in lines: 
        words = line.split()
        for _ in range(n):
            word_to_replace = random.choice(words)
            synonyms = wordnet.synsets(word_to_replace)
            if synonyms:
                synonym = synonyms[0].lemmas()[0].name()
                words = [synonym if word == word_to_replace else word for word in words]
        cleaned_lines.append(' '.join(words))
    return '\n'.join(cleaned_lines)


def random_deletion(text, deletion_prob=0.2):
    # Randomly remove words from the text to create new variations.
    with open(text, 'r') as f:
        lines = f.readlines()
    cleaned_lines = []
    for line in lines: 
        words = line.split()
        new_words = [word for word in words if random.random() > deletion_prob]
        cleaned_lines.append(' '.join(new_words))
    return '\n'.join(cleaned_lines)

def random_insertion(text):
    # Insert random words into the text to create new sentences.
    with open(text, 'r') as f:
        lines = f.readlines()
    cleaned_lines = []
    for line in lines: 
        words = line.split()
        random_word = random.choice(words)
        words.insert(random.randint(0, len(words)), random_word)
        cleaned_lines.append(' '.join(words))
    return '\n'.join(cleaned_lines)

def random_swap(text):
    # Randomly swap words in the text to create new variations.
    with open(text, 'r') as f:
        lines = f.readlines()
    cleaned_lines = []
    for line in lines: 
        words = line.split()
        if len(words) < 2:
            cleaned_lines.append(line)
        else:
            idx1, idx2 = random.sample(range(len(words)), 2)
            words[idx1], words[idx2] = words[idx2], words[idx1]
            cleaned_lines.append(' '.join(words))
    return '\n'.join(cleaned_lines)