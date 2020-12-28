import MeCab
from gensim import matutils
from gensim.corpora import Dictionary
import numpy as np
from scipy.sparse import csr_matrix


def split_into_words(text:str, only_noun=False, pick_feature=None):
    if text is None:
        return []
    if not isinstance(text,str):
        return []
    tagger = MeCab.Tagger("-Owakati")
    tagger.parse('')
    node = tagger.parseToNode(text)
    words = []
    while node:
        if only_noun:
            feature = node.feature.split(",")
            if feature[0] != "名詞":
                node = node.next
                continue
        if pick_feature or len(pick_feature)>0:
            feature = node.feature.split(",")
            if feature[0] not in pick_feature:
                node = node.next
                continue
        word = node.surface
        words.append(word)
        node = node.next
    return words



def dictionary(words, no_below=None, no_above=None) -> Dictionary:
    # Dictionary は単語の配列の配列を受け付ける
    d = None
    if isinstance(words, (list, tuple, np.ndarray, csr_matrix)):
        if isinstance(words[0], (list, tuple, np.ndarray, csr_matrix)):
            d = Dictionary(words)
        else:
            d = Dictionary([words])
    else:
        print(type(words))
        print(type(words[0]))
        raise TypeError("words=には、strの配列あるいはstrの配列の配列を入力してください。")
    # no_below: 使われてる文章がno_below個以下の単語無視
    # no_above: 使われてる文章の割合がno_above以上の場合無視
    # print(dictionary.token2id)
    if no_above:
        if no_below:
            d.filter_extremes(no_below=no_below, no_above=no_above)
        else:
            d.filter_extremes(no_above=no_above)
    else:
        if no_below:
            d.filter_extremes(no_below=no_below)
    print(d)
    print("no_below = " + str(no_below) + " , no_above = " + str(no_above) )
    return d


def words_to_dense(dictionary: Dictionary, words: list) -> np.ndarray:
    tmp = dictionary.doc2bow(words)
    dense = matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0]
    return dense


def words_to_sparse(dictionary: Dictionary, words: list) -> csr_matrix:
    tmp = dictionary.doc2bow(words)
    dense = matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0]
    return csr_matrix(dense)


def text_to_sparse(dictionary: Dictionary, text: str) -> csr_matrix:
    words = split_into_words(text)
    tmp = dictionary.doc2bow(words)
    dense = matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0]
    return csr_matrix(dense)


