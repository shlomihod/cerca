# -*- coding: utf-8 -*- 

def preprocess_es(word):
    return word.replace('ll', 'y') \
               .replace('ch', 'ts') \
               .replace('z', 's')