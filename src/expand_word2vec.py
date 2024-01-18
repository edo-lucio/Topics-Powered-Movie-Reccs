from gensim.models import KeyedVectors, Word2Vec
from gensim.utils import simple_preprocess
from helpers import get_text
from concurrent.futures import ProcessPoolExecutor

model_path = 'GoogleNews-vectors-negative300.bin'
word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=True, limit=100000)
new_model = Word2Vec(vector_size=300, window=5, min_count=1, workers=4) 

def update_word_vectors(word):
    if word in word2vec_model:
        new_model.wv[word] = word2vec_model[word]

if __name__ == "__main__":
    text = get_text()
    sentences = [simple_preprocess(x) for x in text]
    new_model.build_vocab(sentences)

    with ProcessPoolExecutor(max_workers=12) as executor:  
        executor.map(update_word_vectors, new_model.wv.index_to_key)

    new_model.save('expa_model')
