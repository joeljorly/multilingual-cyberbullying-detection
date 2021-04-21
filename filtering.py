import re
from nltk import word_tokenize
from ml2en import ml2en
from spellchecker import SpellChecker
from nltk.stem import PorterStemmer

SPELL = SpellChecker()
STEM = PorterStemmer()


class Filter:
    def __init__(self):
        pass

    def filtering(self):
        text = open("data/comments.txt", "r").read()
        text = self.remove_emoji(text)
        pattern_rem = self.pattern(text)
        file = open('filter.txt', 'w')
        lines = pattern_rem.splitlines()
        for line in lines:
            if len(line) != 0:
                split = line.split()
                for word in split:
                    if word[0] != '@':
                        file.write(word+' ')
                file.write('\n')
        file.close()
        file1 = open('filter.txt', 'r').readlines()
        file2 = open('filter.txt', 'w')

        for i in file1:
            if i == '\n':
                continue
            rec = self.remove(i)
               # print(rec)
            if rec == None or rec == " ":
                    continue
                
            ma_en = ml2en.transliterate(self.pattern(rec))
            # ml_only=eng(ma_en)
            file2.write(ma_en+"\n")
            # file2.write('\n')
        file2.close()

    def remove_emoji(self, sen):  # remove emojis
        emoji_pattern = re.compile("[" u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030" "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r' ', sen)

    def pattern(self, rem_pattern):  # remove punctuations in the text
        punc = '''!-;:'",()./?#$%'''

        for ele in rem_pattern:
            if ele in punc:
                rem_pattern = rem_pattern.replace(ele, " ")
        rem_pattern = re.sub(' +', ' ', rem_pattern)

        # remove empty lines between text
        return '\n'.join([i for i in rem_pattern.split('\n') if len(i) > 0])

    def remove(self, sent):  # remove english sentences from the dataset so their will be only manglish and malayalam
        word_file = open("data/words.txt", "r").readlines()
        count = 0
        char = ""
        token = word_tokenize(sent)
        if token[0].isalnum() == False:
            for i in token:
                # print(i,end=' ')
                char = char+i+" "
            return char
        for check in token:
            misspelled = SPELL.unknown([check])
            for j in misspelled:
                check = SPELL.correction(j)
                check = STEM.stem(check)
            for l in word_file:
                if l[:-1] == check.lower():
                    # print(w)
                    count = count+1
        if count != len(token):
            print(sent, end=" ")
            return sent


word = Filter()
word.filtering()
