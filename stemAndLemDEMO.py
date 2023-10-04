# regex for removing punctuation
import re

# nltk preprocessing
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# grabbing a part of speech function:
# from part_of_speech import get_part_of_speech

text = input("Text to process:\n")

# Remove whitespace and punctuation
cleaned = re.sub('\W+', ' ', text)

# Tokenize
tokenized = word_tokenize(cleaned)

# Stem
stemmer = PorterStemmer()
stemmed = [stemmer.stem(token) for token in tokenized]

# Lemmatize
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(token) for token in tokenized]

# Print stemmed text
print("Stemmed text:")
print(stemmed)

# Print lemmatized text
print("\nLemmatized text:")
print(lemmatized)
