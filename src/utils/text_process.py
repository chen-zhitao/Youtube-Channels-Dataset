from langdetect import detect
import re
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

def is_english(text):
    lang=detect(text)
    return lang== 'en'

# see the following discussion for setting up language processing factory in Spacy
# https://stackoverflow.com/questions/66712753/how-to-use-languagedetector-from-spacy-langdetect-package

@Language.factory("language_detector")
def get_lang_detector(nlp, name):
    return LanguageDetector()


def get_nlp():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe('language_detector', last=True)
    return nlp


def preprocess_text(text, nlp):
    
    doc = nlp(text)
    
    filtered_sentences = []
    for sentence in doc.sents:
        # remove non-English sentences or sentences containing urls, emails, or social handles
        if sentence._.language["language"] != "en":
            continue
        if not any(token.like_url or token.like_email or token.text.startswith('@') for token in sentence):
            filtered_sentences.append(sentence.text)
            
    text=' '.join(filtered_sentences)

    # remove special characters from text
    #text=re.sub(r'[^a-zA-Z\s,.!?\'\"]', ' ', text)
    text=re.sub(r'[^a-zA-Z\s,.!?]', ' ', text)

    # remove extra empty space between sentences
    text=" ".join(text.split())

    return text
