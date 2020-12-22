import re
import nltk
import heapq
import spacy
import bs4 as bs
import urllib.request
from collections import Counter
# python -m spacy download de_core_news_sm
import de_core_news_sm
from textblob_de import TextBlobDE

nlp_de = de_core_news_sm.load()


def get_text(link):
    scraped_text = urllib.request.urlopen(link).read()
    soup_text = bs.BeautifulSoup(scraped_text,'lxml')
    paragraphs = soup_text.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    # print(article_text)
    return article_text


def preprocess_text(txt):
    f = open(txt, "r")
    f_read = f.read()
    text = nlp_de(f_read)
    return text


def analyse_sentiment(text):
    text_polarity = round(TextBlobDE(str(text)).sentiment.polarity, 3)
    text_subjectivity = round(TextBlobDE(str(text)).sentiment.subjectivity, 3)
    print("Text Sentiment:", text_polarity)
    print("Text Subjektivität:", text_subjectivity)


def extract_entities(text):
    text = nlp_de(text)
    entities_nr = len(text.ents)
    print(entities_nr, "Entities in diesem Text.")

    entities_labels = Counter([x.label_ for x in text.ents])
    print(entities_labels)

    entities_top3 = Counter([x.text for x in text.ents]).most_common(3)
    print("Die 3 häufigsten Entities:\n", entities_top3)

    entities_list = [(X.text, X.label_) for X in text.ents]
    print("Entities im Text:\n", entities_list)


def get_lexical_richness(text):
    lex_rich = round(len(set(text))/len(text), 3)
    print("Lexikalische:", lex_rich)


def summarize_text(text):
    article_text = preprocess_text("app/texts/example1.txt")
    article_text = str(article_text)

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words('german')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
        maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    print("Zusammenfassung:\n", summary)


if __name__ == "__main__":
    # input_text = preprocess_text("app/texts/example1.txt")
    link = 'https://www.bundesregierung.de/breg-de/aktuelles/reden/rede-von-bundeskanzlerin-merkel-zum-startschuss-fuer-das-ai-breakthrough-hub-am-17-dezember-2020-videokonferenz--1829778'
    input_link = input("Link: ")
    input_text = get_text(input_link)
    analyse_sentiment(input_text)
    extract_entities(input_text)
    get_lexical_richness(input_text)
    summarize_text(input_text)
