import MeCab
from gensim import matutils
from gensim.corpora import Dictionary


def split_into_words (text):
    tagger = MeCab.Tagger("-Owakati")
    node = tagger.parseToNode(text)
    words = []
    while node:
        word = node.surface
        words.append(word)
        node = node.next
    return words


def words_to_dense(dictionary: Dictionary, words: list):
    tmp = dictionary.doc2bow(words)
    dense = matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0]
    return dense




