import pytest
from src.mask_tools import mask_text as mt


def test_split_into_words():
    words = mt.split_into_words('筑波は関東にある', only_noun=True)
    assert words[0] == '筑波'
    assert words[1] == '関東'


def test_dictionary():
    with pytest.raises(TypeError):
        mt.dictionary('aaa')


def test_words_to_sparse():
    dictionary = mt.dictionary(['aaa','bbb','ccc'])
    dense = mt.words_to_sparse(dictionary,['aaa','bbb'])


if __name__ == '__main__':
    test_split_into_words()
    test_dictionary()
    test_words_to_sparse()
