# -*- coding: utf-8 -*-
import operator
import logging
import re
import string
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize

logging.basicConfig(filename="logs/Preprocessingclass.log",
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w')

# https://pypi.org/project/pyspellchecker/
spell = SpellChecker(language=None, case_sensitive=True, distance=2)
# changed the parameters of SpellChecker for adding custom dictionary

fd = open('data/maglish.txt').readlines()
out = open("pre_out.txt", "w")
file = open("filter.txt", "r")


class preprocess:
    def __init__(self):
        self.preprocessing()

    def preprocessing(self):
        output = []
        c = 0
        for read in file:
            self.tokens(read)

    def tokens(self, read):
        try:
            list_len = 0
            filter = '\n\u200c\u200d '
            l = []
            token = word_tokenize(read)
            output = []
            c = 0
            for one in range(0, len(token)):
                try:
                    token[c] = self.remove(token[c]).lower()
                    logging.info("word tokenization completed")
                except:
                    pass
                for i in fd:
                    if operator.contains(i, token[c]):
                        l.append(i)
                logging.info("pattern finding")
                # print("list",l)

                if len(l) > 0:
                    for j in l:
                        for k in j:
                            if k in filter:
                                j = j.replace(k, "")
                        if token[c] == j:
                            # print("equal",j)
                            output.append(j)
                            out.write(self.slang(j)+" ")
                            break
                        list_len = list_len+1
                    logging.info("pattern matching")
                    if list_len == len(l):
                        spell.word_frequency.load_text_file('data/maglish.txt')
                        misspelled = spell.unknown([token[c]])
                        for word in spell.candidates(token[c]):
                            if word == token[c]:
                                #print("not in",token[c])
                                output.append(token[c])
                                out.write(self.slang(token[c])+" ")
                            else:
                                for j in misspelled:
                                  # print(spell.correction(j))
                                    output.append(spell.correction(j))
                                  # print(spell.candidates(j))
                                    out.write(self.slang(
                                        spell.correction(j))+" ")
                            break
                        logging.info("spell checking and correction")
                else:
                    spell.word_frequency.load_text_file('data/maglish.txt')
                    misspelled = spell.unknown([token[c]])
                    for word in spell.candidates(token[c]):
                        if word == token[c]:
                            #print("not in",token[c])
                            output.append(token[c])
                            out.write(self.slang(token[c])+" ")
                        else:
                            for j in misspelled:
                                # print(spell.correction(j))
                                output.append(spell.correction(j))
                                # print(spell.candidates(j))
                                out.write(self.slang(spell.correction(j))+" ")
                        break
                    logging.info("spell checking and correction")
                c = c+1
                l = []
                list_len = 0
            out.write("\n")
            logging.debug(output)
            return output
        except:
            logging.warning("error may be encountered")

    def remove(self, word):
        i = len(word)-1
        while i >= 3:
            if word[i] == word[i-1] and word[i-1] == word[i-2]:
                word = word[:i]+word[i+1:]
                i = len(word)-1
            else:
                i = i-1
        if word[-1] == word[-2]:
            word = word[:-1]
        return word

    def slang(self, word):
        if word in ['myr', 'myratthi', 'myre', 'myrolii', 'myrandi', 'myrinte', 'myrethik', 'myroli', 'mythandi']:
            return 'myre'
        if word in ['puri', 'purimone', 'poorimol', 'poori', 'pookachi', 'pundachi', 'puthichi', 'pulayadi']:
            return 'poori'
        if word in ['poli', 'pole', 'adepoyla', 'adipowli', 'pwoli', 'poliyanallo', 'policchu', 'pwolichu', 'pwolich', 'adipoli', 'polikadi', 'polichutto', 'poliyannu', 'polichada']:
            return 'poli'
        if word in ['kundioli', 'kundi', 'kundiyle', 'kundipenne', 'kundiyadi', 'kundika', 'kundiyoliye']:
            return 'kundi'
        if word in ['tholvikal', 'tholvi']:
            return 'tholvi'
        if word in ['vanam', 'vaanam', 'maravaanam', 'valiyavanaada']:
            return 'vanam'
        if word in ['thendikal', 'thendi']:
            return 'thendi'
        if word in ['marappattikal', 'patti', 'paatti', 'pattika', 'naaye']:
            return 'patti'
        if word in ['naariya', 'naari', 'nari']:
            return 'naari'
        if word in ['ishtam', 'ishtamaanennu', 'ishtangal', 'ishta', 'ishtappedunnath', 'ishtaayi', 'estam']:
            return 'ishtaayi'
        if word in ['muthea', 'muth', 'mwuthumani', 'mwuthmanye', 'muthe', 'mani', 'mutimani', 'mwuthe']:
            return 'mwuthe'
        if word in ['kiduve', 'kidu', 'kitukki', 'kidiloski', 'kidukki', 'kalakki']:
            return 'kidu'
        if word in ['kolam', 'koolam', 'kollaam']:
            return 'kollaam'
        if word in ['levelatta', 'levelu', 'level']:
            return 'level'
        if word in ['charakkalle', 'charakkale']:
            return 'charakkalle'
        if word in ['koppanmare', 'koppe']:
            return 'koppe'
        if word in ['mulacchi', 'mulaaaas', 'mulaas', 'mulas']:
            return 'mulaas'
        if word in ['oomb', 'oombiya', 'oombi', 'ooombiya']:
            return 'oomb'
        if word in ['chathude', 'chathoodadai', 'chathille', 'chathoode', 'chavina']:
            return 'chathude'
        if word in ['vattanenki', 'vattan', 'vattaayi', 'bhraanthaataa', 'vatta', 'vata']:
            return 'vatta'
        if word in ['boraayittundu', 'bore']:
            return 'bore'
        if word in ['dislike', 'dis‌lykku', 'dis‌lykkum']:
            return 'dislike'
        if word in ['durantham', 'duranthamaayi']:
            return 'durantham'
        if word in ['kunna', 'koona', 'kunne']:
            return 'kunna'
        if word in ['kooppu', 'koppanmaree']:
            return 'kooppu'
        if word in ['lookaada', 'look']:
            return 'look'
        if word in ['nallathu', 'nalla', 'nanayitund']:
            return 'nalla'
        if word in ['otthiri', 'orumpaatu']:
            return 'otthiri'
        if word in ['sadhajaaram', 'sadajara', 'sathajara']:
            return 'sadhajaaram'
        if word in ['sundari', 'sundhaaaaaari', 'sundharii']:
            return 'sundari'
        if word in ['supar', 'sooppar']:
            return 'supar'
        if word in ['supportaayit', 'support']:
            return 'support'
        if word in ['thallakku', 'thala']:
            return 'thala'
        if word in ['thoori', 'thittam']:
            return 'thittam'
        if word in ['undalla', 'undavum']:
            return 'undalla'
        return word


preprocess()
