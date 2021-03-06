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
    """Function that scrapes the text in every paragraph
    from a link to bundesregierung.de website."""

    scraped_text = urllib.request.urlopen(link).read()
    soup_text = bs.BeautifulSoup(scraped_text, "lxml")
    paragraphs = soup_text.find_all("p")
    article_text = ""
    for p in paragraphs:
        article_text += p.text

    return article_text


def preprocess_text(txt):
    """Function that processes the text
    from an input text file.
    """

    f = open(txt, "r")
    f_read = f.read()
    text = nlp_de(f_read)
    return text


def analyse_sentiment(text):
    """Function that returns the polarity and subjectivity
    of a preprocessed scraped text."""

    text_polarity = round(TextBlobDE(str(text)).sentiment.polarity, 3)
    text_subjectivity = round(TextBlobDE(str(text)).sentiment.subjectivity, 3)

    return "Polarität:", text_polarity, "Subjektivität:", text_subjectivity


def extract_entities(text):
    """Function that extracts the entities from a scraped text
    and returns the count and list of entities."""

    text = nlp_de(text)
    entities_nr = len(text.ents)
    # print(entities_nr, "Entities in diesem Text.")
    entities_labels = Counter([x.label_ for x in text.ents])
    entities_top3 = Counter([x.text for x in text.ents]).most_common(3)
    entities_list = [(X.text, X.label_) for X in text.ents]

    return (
        entities_nr,
        "Entities in diesem Text:",
        entities_labels,
        "Die 3 häufigsten Entities:\n",
        entities_top3,
        "Identifizierte Entities:\n",
        entities_list,
    )


def get_lexical_richness(text):
    """Function that calculates the lexical richness
    of a scraped text."""

    lex_rich = round(len(set(text)) / len(text), 3)
    return "Lexikalische Vielfalt:", lex_rich


def summarize_text(text):
    """Function that preprocesses a scraped text
    and returns a summary of the text."""

    # article_text = preprocess_text("app/texts/example1.txt")
    # article_text = str(article_text)

    text = re.sub(r"\[[0-9]*\]", " ", text)
    text = re.sub(r"\s+", " ", text)

    formatted_text = re.sub("[^a-zA-Z]", " ", text)
    formatted_text = re.sub(r"\s+", " ", formatted_text)
    sentence_list = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words("german")

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
        maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / maximum_frequncy
        sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = " ".join(summary_sentences)
    return "Zusammenfassung:\n", summary


if __name__ == "__main__":
    # input_text = preprocess_text("app/texts/example1.txt")
    # link = 'https://www.bundesregierung.de/breg-de/aktuelles/reden/rede-von-bundeskanzlerin-merkel-zum-startschuss-fuer-das-ai-breakthrough-hub-am-17-dezember-2020-videokonferenz--1829778'
    input_link = input("Link: ")
    input_text = get_text(input_link)
    sentiment = str(analyse_sentiment(input_text))
    entities = str(extract_entities(input_text))
    lexic = str(get_lexical_richness(input_text))
    summary = str(summarize_text(input_text))

    full_text = (
        "Quelle:"
        + str(input_link)
        + input_text
        + "\n"
        + sentiment
        + "\n"
        + entities
        + "\n"
        + lexic
        + "\n"
        + summary,
    )

    with open("app/texts/output.txt", "w") as f:
        f.writelines(full_text)