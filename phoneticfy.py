# -*- coding: utf-8 -*- 

import sys

from metaphone import doublemetaphone

from tqdm import tqdm

from cerca import db
from models import PhoneticWord, LangWord

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def build_similar_phonetic_words_db(lang, wordslist_path):
    with open(wordslist_path, 'rb') as wordslist_file:
        wordslist = [w.strip().lower() for w in wordslist_file.read().splitlines()]
    
    for word in tqdm(wordslist):

        phonetic_primary, phonetic_secondary = doublemetaphone(word)
        
        phonetic_word_primary = None
        phonetic_word_secondary = None

        if phonetic_primary:
            phonetic_word_primary = get_or_create(db.session,
                                                  PhoneticWord,
                                                  phonetic=phonetic_primary)
            
        if phonetic_secondary:
            phonetic_word_secondary = get_or_create(db.session,
                                              PhoneticWord,
                                              phonetic=phonetic_secondary)
        if phonetic_word_primary is not None or \
            phonetic_word_secondary is not None:

            lang_word = get_or_create(db.session,
                                      LangWord,
                                      lang=lang,
                                      word=word,
                                      phonetic_word_primary=phonetic_word_primary,
                                      phonetic_word_secondary=phonetic_word_secondary)
                
            
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    build_similar_phonetic_words_db(sys.argv[1], sys.argv[2])