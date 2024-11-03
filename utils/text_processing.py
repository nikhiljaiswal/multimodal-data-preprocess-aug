import re 
from nltk.corpus import stopwords
from torchtext.data.utils import get_tokenizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer() 
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def tokenize(text):
    # Tokenization logic
    with open(text, 'r') as f:
        lines = f.readlines()
    tokenizer = get_tokenizer('basic_english')
    tokens = [' '.join(tokenizer(line)) for line in lines]
    return '\n'.join(tokens)

def padding_truncating(text):
    PAD_TOKEN = '<PAD>'
    # Padding/Truncating logic
    with open(text, 'r') as f:
        lines = f.readlines()
    max_length = max([len(str(s).split()) for s in lines])
    op=[]
    for line in lines:
        line = str(line).split()
        if len(line) < max_length:
            line = line + [PAD_TOKEN]*(max_length - len(line))
        op.append(' '.join(line))
    return '\n'.join(op)

def lowercase(text):
    with open(text, 'r') as f:
        lines = f.readlines()
    op = [str(s).lower().strip() for s in lines]
    return '\n'.join(op)

def remove_stopwords(text):
    with open(text, 'r') as f:
        lines = f.readlines()
    cleaned_lines = []
    for line in lines:
        words = word_tokenize(line)
        filtered_words = [word for word in words if word.lower() not in stop_words]
        cleaned_line = ' '.join(filtered_words)
        cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)

def noise_removal(text):
    with open(text, 'r') as f:
        lines = f.readlines()
    op = []
    for line in lines:
        line = re.sub(r'[^a-zA-Z\s]', '', line)
        op.append(line)
    return '\n'.join(op)

def perform_stemming(text):
    with open(text, 'r') as f:
        lines = f.readlines()
    op = []
    for line in lines:
        line = [ps.stem(word) for word in line.split()]
        op.append(' '.join(line))
    return '\n'.join(op)

def perform_lemmatization(text):
    with open(text, 'r') as f:
        lines = f.readlines()
    op = []
    for line in lines:
        line = [lemmatizer.lemmatize(word) for word in line.split()]
        op.append(' '.join(line))
    return '\n'.join(op)


