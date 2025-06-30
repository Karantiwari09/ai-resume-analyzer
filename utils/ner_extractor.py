import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_entities(resume_text):
    doc = nlp(resume_text)
    entities = {"PERSON": [], "ORG": [], "GPE": [], "EMAIL": [], "DATE": [], "SKILL": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities
