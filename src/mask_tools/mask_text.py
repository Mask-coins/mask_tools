import MeCab
from gensim import matutils
from gensim.corpora import Dictionary


def split_into_words(text, only_noun=False):
    tagger = MeCab.Tagger("-Owakati")
    node = tagger.parseToNode(text)
    words = []
    while node:
        if only_noun:
            feature = node.feature.split(",")
            if feature[0] != "名詞":
                node = node.next
                continue
        word = node.surface
        words.append(word)
        node = node.next
    return words


def words_to_dense(dictionary: Dictionary, words: list):
    tmp = dictionary.doc2bow(words)
    dense = matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0]
    return dense




