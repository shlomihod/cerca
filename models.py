# -*- coding: utf-8 -*- 

from cerca import db

class PhoneticWord(db.Model):
    __tablename__ = 'phonetic_words'

    id = db.Column(db.Integer, primary_key=True)
    phonetic = db.Column(db.String())
    
    def __init__(self, phonetic):
        self.phonetic = phonetic
    
    def __repr__(self):
        return '<id {} = {}>'.format(self.id, self.phonetic)


class LangWord(db.Model):
    __tablename__ = 'lang_words'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String())
    word = db.Column(db.String())

    phonetic_word_primary_id = db.Column(db.Integer, db.ForeignKey('phonetic_words.id'), nullable=False)
    phonetic_word_primary = db.relationship('PhoneticWord',  foreign_keys=[phonetic_word_primary_id],
        backref=db.backref('lang_words_primary', lazy='dynamic'))
    
    phonetic_word_secondary_id = db.Column(db.Integer, db.ForeignKey('phonetic_words.id'))
    phonetic_word_secondary = db.relationship('PhoneticWord',  foreign_keys=[phonetic_word_secondary_id],
        backref=db.backref('lang_words_secondary', lazy='dynamic'))
    

    def __init__(self, lang, word, phonetic_word_primary, phonetic_word_secondary=None):
        self.lang = lang
        self.word = word
        self.phonetic_word_primary = phonetic_word_primary

    def __repr__(self):
        return '<id {} {} {} {}>'.format(self.id, self.lang, self.word, self.phonetic_word_primary)