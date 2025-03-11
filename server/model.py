import gensim
from gensim.utils import simple_preprocess
import pandas as pd
import numpy as np
import random
from time import time

from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')

wiki = pd.read_csv('wikipedia_sentences_2.csv')


# #save all words into a list so we can randomly choose the target word later
# word_list = [word.lower() for word in words['English'].tolist()]
# print(len(word_list))

#convert sentences into a list
sentences_list = wiki.iloc[:, 0].tolist()
print(f"totla number of sentences {len(sentences_list)}")

#from gensim library, it tokenizes (splits input into words on spaces), converts all words to lowercase, and removes words with less than 2 letters or more than 15 letters.
clean_sentences = [simple_preprocess(sentence) for sentence in sentences_list]


# removing stop words
stop_words = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can't", "cannot","could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing",
    "don't", "down", "during", "each", "few", "for", "from", "further", "had","hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd",
    "he'll", "he's", "her", "here", "here's", "hers", "herself", "him","himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if",
    "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves","out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's",
    "should", "shouldn't", "so", "some", "such", "than", "that", "that's","the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've","this", "those", "through", "to", "too", "under", "until", "up", "very",
    "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were","weren't", "what", "what's", "when", "when's", "where", "where's",
    "which", "while", "who", "who's", "whom", "why", "why's", "with","won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves"
]

for sentence in clean_sentences:
    sentence[:] = [word for word in sentence if word not in stop_words]


#Lemmatization reduces words to their base form (e.g., "apples" → "apple", "berries" → "berry").
lemmatizer = WordNetLemmatizer()
clean_sentences = [
    [lemmatizer.lemmatize(word) for word in simple_preprocess(sentence) if word not in stop_words]
    for sentence in sentences_list
]
#
random.seed(42)
np.random.seed(42)

#word2vec model from gensim library
model = gensim.models.Word2Vec(
    window=5,
    min_count=7,
    workers=1,
    vector_size=120,
    seed=42
)

#bulding one-hot-encoding of our words
model.build_vocab(clean_sentences, progress_per=10)


print(f"number of words in our datasets {len(model.wv)}")


t = time()

#training the model
model.train(clean_sentences, total_examples=model.corpus_count, epochs=30)


print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

print("model was trained over sentences succesfully")

model.save("word2vec.model")

print("model has been saved")