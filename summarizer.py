# Gensim Imports
from gensim.summarization.summarizer import summarize

# Spacy Imports
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# NLTK Imports
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Sumy Imports
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# Other Imports
from string import punctuation
from heapq import nlargest


def gensim_summarize(text_content, percent):
    # TextRank Summarization using Gensim Library.
    # Split is false, gensim return strings joined by "\n". if true, gensim will return list
    summary = summarize(text_content, ratio=(int(percent) / 100), split=False).replace("\n", " ")

    # Returning NLTK Summarization Output
    return summary


def spacy_summarize(text_content, percent):
    # Frequency Based Summarization using Spacy.
    # Build a List of Stopwords
    stop_words = list(STOP_WORDS)

    # import punctuations from strings library.
    punctuation_items = punctuation + '\n'

    # Loading en_core_web_sm in Spacy
    nlp = spacy.load('en_core_web_sm')

    # Build an NLP Object
    nlp_object = nlp(text_content)

    # Create the dictionary with key as words and value as number of times word is repeated.
    # Scoring words by its occurrence.
    word_frequencies = {}
    for word in nlp_object:
        if word.text.lower() not in stop_words:
            if word.text.lower() not in punctuation_items:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    # Finding frequency of most occurring word
    max_frequency = max(word_frequencies.values())

    # Divide Number of occurrences of all words by the max_frequency
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    # Save a sentence-tokenized copy of text
    sentence_token = [sentence for sentence in nlp_object.sents]

    # Create the dictionary with key as sentences and value as sum of each important word.
    # Scoring sentences by its words.
    sentence_scores = {}
    for sent in sentence_token:
        sentence = sent.text.split(" ")
        for word in sentence:
            if word.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.lower()]

    # Finding number of sentences and applying percentage on it: since we require to show most X% lines in summary.
    select_length = int(len(sentence_token) * (int(percent) / 100))

    # Using nlargest library to get the top x% weighted sentences.
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    # Later joining it to get the final summarized text.
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    # Returning NLTK Summarization Output
    return summary


def nltk_summarize(text_content, percent):
    # Frequency Based Summarization using NLTK
    # Store a tokenized copy of text, using NLTK's recommended word tokenizer
    tokens = word_tokenize(text_content)

    # Import the stop words from NLTK toolkit
    stop_words = stopwords.words('english')

    # import punctuations from strings library.
    punctuation_items = punctuation + '\n'

    # Create the dictionary with key as words and value as number of times word is repeated.
    # Scoring words by its occurrence.
    word_frequencies = {}
    for word in tokens:
        if word.lower() not in stop_words:
            if word.lower() not in punctuation_items:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

    # Finding frequency of most occurring word
    max_frequency = max(word_frequencies.values())

    # Divide Number of occurrences of all words by the max_frequency
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    # Save a sentence-tokenized copy of text
    sentence_token = sent_tokenize(text_content)

    # Create the dictionary with key as sentences and value as sum of each important word.
    # Scoring sentences by its words.
    sentence_scores = {}
    for sent in sentence_token:
        sentence = sent.split(" ")
        for word in sentence:
            if word.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.lower()]

    # Finding number of sentences and applying percentage on it: since we require to show most X% lines in summary.
    select_length = int(len(sentence_token) * (int(percent) / 100))

    # Using nlargest library to get the top x% weighted sentences.
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    # Later joining it to get the final summarized text.
    final_summary = [word for word in summary]
    summary = ' '.join(final_summary)

    # Returning NLTK Summarization Output
    return summary


def sumy_lsa_summarize(text_content, percent):
    # Latent Semantic Analysis is a unsupervised learning algorithm that can be used for extractive text summarization.
    # Initializing the parser
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    # Initialize the stemmer
    stemmer = Stemmer('english')
    # Initializing the summarizer
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')

    # Finding number of sentences and applying percentage on it: since sumy requires number of lines
    sentence_token = sent_tokenize(text_content)
    select_length = int(len(sentence_token) * (int(percent) / 100))

    # Evaluating and saving the Summary
    summary = ""
    for sentence in summarizer(parser.document, sentences_count=select_length):
        summary += str(sentence)
    # Returning NLTK Summarization Output
    return summary


def sumy_luhn_summarize(text_content, percent):
    # A naive approach based on TF-IDF and looking at the “window size” of non-important words between words of high
    # importance. It also assigns higher weights to sentences occurring near the beginning of a document.
    # Initializing the parser
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    # Initialize the stemmer
    stemmer = Stemmer('english')
    # Initializing the summarizer
    summarizer = LuhnSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')

    # Finding number of sentences and applying percentage on it: since sumy requires number of lines
    sentence_token = sent_tokenize(text_content)
    select_length = int(len(sentence_token) * (int(percent) / 100))

    # Evaluating and saving the Summary
    summary = ""
    for sentence in summarizer(parser.document, sentences_count=select_length):
        summary += str(sentence)
    # Returning NLTK Summarization Output
    return summary


def sumy_text_rank_summarize(text_content, percent):
    # TextRank is an unsupervised text summarization technique that uses the intuition behind the PageRank algorithm.
    # Initializing the parser
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    # Initialize the stemmer
    stemmer = Stemmer('english')
    # Initializing the summarizer
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')

    # Finding number of sentences and applying percentage on it: since sumy requires number of lines
    sentence_token = sent_tokenize(text_content)
    select_length = int(len(sentence_token) * (int(percent) / 100))

    # Evaluating and saving the Summary
    summary = ""
    for sentence in summarizer(parser.document, sentences_count=select_length):
        summary += str(sentence)
    # Returning NLTK Summarization Output
    return summary
