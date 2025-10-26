import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt', quiet=True)

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
    return " ".join(sentences[:num_sentences])
