def summarize_text(text):
    pass

def extract_entities(txt):
    f = open(txt, "r")
    f_read = f.read()
    text = nlp_de(f_read)
    
    entities_list = [(X.text, X.label_) for X in text.ents]
    return entities_list

def analyse_sentiment(text):
    pass