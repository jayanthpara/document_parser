from heapq import nlargest
from collections import defaultdict
import re

def summarize_text(text, sentences_count=5):
    # Split into sentences using a simple regex (offline alternative to nltk.sent_tokenize)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) <= sentences_count:
        return text

    # Create a frequency table for words
    word_freq = defaultdict(int)
    for word in re.findall(r'\w+', text.lower()):
        if len(word) > 3:
            word_freq[word] += 1

    # Score each sentence based on word frequency
    sentence_scores = {}
    for sent in sentences:
        for word in re.findall(r'\w+', sent.lower()):
            if word in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word]

    # Select top N sentences
    top_sentences = nlargest(sentences_count, sentence_scores, key=sentence_scores.get)
    return ' '.join(top_sentences)
