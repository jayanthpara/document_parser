import re
from heapq import nlargest
from collections import defaultdict

def summarize_text(text, sentences_count=5):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) <= sentences_count:
        return text
    word_freq = defaultdict(int)
    for word in re.findall(r'\w+', text.lower()):
        if len(word) > 3:
            word_freq[word] += 1
    sentence_scores = {}
    for sent in sentences:
        for word in re.findall(r'\w+', sent.lower()):
            sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word]
    top_sentences = nlargest(sentences_count, sentence_scores, key=sentence_scores.get)
    return ' '.join(top_sentences)
