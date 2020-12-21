import spacy
from collections import Counter
import de_core_news_sm
from textblob_de import TextBlobDE

nlp_de = de_core_news_sm.load()

def preprocess_text(txt):
    f = open(txt, "r")
    f_read = f.read()
    text = nlp_de(f_read)
    return text

def analyse_sentiment(text):
    text_polarity = round(TextBlobDE(str(text)).sentiment.polarity, 3)
    text_subjectivity = round(TextBlobDE(str(satz)).sentiment.subjectivity, 3)
    print("Text Sentiment:", text_polarity)
    print("Text Subjektivität:", text_subjectivity)

def summarize_text(text):
    pass



def extract_entities(text):
    entities_nr = len(text.ents)
    print(entities_nr, "Entities in diesem Text.")

    entities_labels = Counter([x.label_ for x in text.ents])
    print(entities_labels)

    entities_top3 = Counter([x.text for x in text.ents]).most_common(3)
    print("Die 3 häufigsten Entities:\n", entities_top3)

    entities_list = [(X.text, X.label_) for X in text.ents]
    print("Entities im Text:\n", entities_list)


if __name__ == "__main__":
    input_text = preprocess_text("app/texts/example1.txt")
    analyse_sentiment(input_text)
    extract_entities(input_text)