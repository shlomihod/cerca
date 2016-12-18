# -*- coding: utf-8 -*- 

import os

from microsofttranslator import Translator
from metaphone import doublemetaphone

from flask import Flask, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

from models import PhoneticWord, LangWord

from preprocess_metaphone import preprocess_es

translator = Translator(os.environ['CERCA_MST_ID'],os.environ['CERCA_MST_SECRET'])

SUPPORTED_SRC_LANGUAGES = ['es']
SUPPORTED_DST_LANGUAGES = ['en']

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/transform/<src_lang>/<dst_lang>/<src_word>')
def transform(src_lang, dst_lang, src_word):

    src_word = src_word.lower()

    if dst_lang not in SUPPORTED_DST_LANGUAGES or src_lang not in SUPPORTED_SRC_LANGUAGES:
        abort(404)

    translated_word = translator.translate(src_word, dst_lang, src_lang)

    all_similar_phonetic_words = get_all_similar_phonetic_words(dst_lang, src_word)

    return jsonify(translatedWord   =   translated_word,
                   similarPhoneticWord = all_similar_phonetic_words)

def get_similar_phonetic_words(dst_lang, phonetic):
    similar_phonetic_words = []

    phonetic_word = PhoneticWord.query.filter_by(phonetic=phonetic).first()

    if phonetic_word:
        similar_phonetic_words = phonetic_word.                \
                                    lang_words_primary.         \
                                    filter_by(lang=dst_lang).  \
                                    all()

        if not similar_phonetic_words:
            similar_phonetic_words = phonetic_word.                \
                                        lang_words_secondary.       \
                                        filter_by(lang=dst_lang).  \
                                        all()

    return similar_phonetic_words


def get_all_similar_phonetic_words(dst_lang, src_word):

    similar_phonetic_words = []

    src_word = preprocess_es(src_word)
    phonetic_primary, phonetic_secondary = doublemetaphone(src_word)

    if phonetic_primary:
        similar_phonetic_words = get_similar_phonetic_words(dst_lang, phonetic_primary)

    if (not similar_phonetic_words or not phonetic_primary) and phonetic_secondary:
        similar_phonetic_words = get_similar_phonetic_words(dst_lang, phonetic_secondary)

    return [lang_word.word for lang_word in similar_phonetic_words]
