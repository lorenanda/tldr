import spacy
from spacy import displacy
from collections import Counter
import de_core_news_sm

nlp_de = de_core_news_sm.load()

def summarize_text(text):
    pass

def extract_entities(txt):
    f = open(txt, "r")
    f_read = f.read()
    text = nlp_de(f_read)
    
    entities_nr = len(text.ents)
    print(entities_nr, "Entities in diesem Text.")

    entities_labels = Counter([x.label_ for x in text.ents])
    print(entities_labels)

    entities_top3 = Counter([x.text for x in text.ents]).most_common(3)
    print("Die 3 häufigsten Entities:\n", entities_top3)

    entities_list = [(X.text, X.label_) for X in text.ents]
    print("Entities im Text:\n", entities_list)

def analyse_sentiment(text):
    pass