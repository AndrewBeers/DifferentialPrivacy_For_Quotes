import os
import glob
import csv
import math
import nltk
import numpy as np
import pickle

from pprint import pprint
from collections import defaultdict
from nltk.tokenize import word_tokenize


class RiskEvaluator(object):

    def __init__(self):

        # Derived Parameters
        self.ngram_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data/ngram_frequencies')
        self.reference_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data/reference_scores.pkl')
        self.ngram_data = defaultdict(dict)
        self.reference_scores = {}
        self.highest_probability = {}
        self.lowest_probability = {}
        self.total_probability = defaultdict(float)
        self.probability_range = {}
        self.n_gram_limit = 2
        self.word_total = 1024908267229  # Adjust code later to accoutn

        return

    def load_dataset(self, ngram_filepath=None):

        if ngram_filepath is None:
            ngram_filepath = self.ngram_filepath

        for n in range(1, self.n_gram_limit + 1):
            print(f'Compiling {n} grams')
            with open(os.path.join(ngram_filepath, f'count_{n}w.txt'), 'r') as readfile:
                reader = csv.reader(readfile, delimiter='\t')
                for line in reader:
                    log_probability = math.log(float(line[1]) / self.word_total)
                    self.ngram_data[n][line[0]] = log_probability
                    self.total_probability[n] += log_probability

            # Note: in Python 3, dictionary keys are ordered.
            self.highest_probability[n] = self.ngram_data[n][list(self.ngram_data[n].keys())[0]]
            self.lowest_probability[n] = self.ngram_data[n][list(self.ngram_data[n].keys())[-1]]
            self.probability_range[n] = [self.lowest_probability[n], self.highest_probability[n]]

        with open(self.reference_filepath, 'rb') as f:
            self.reference_scores = pickle.load(f)

    def evaluate_quote(self, quote):

        text_tokens = word_tokenize(quote)

        # Remove punctuation, lower case
        text_tokens = [word.lower() for word in text_tokens if word.isalpha()]

        # TODO: Ask Tev'n about best practices for stop words.
        # text_tokens = ['<S>'] * min(0, self.n_gram_limit - 2) + text_tokens

        # Determine word probabilities
        probabilities = defaultdict(list)
        ngram_tokens = {}
        for n in range(1, self.n_gram_limit + 1):
            ngram_tokens[n] = list(get_ngrams(text_tokens, n))
            for token in ngram_tokens[n]:
                token = ' '.join(token)
                try:
                    probabilities[n] += [self.ngram_data[n][token]]
                except:
                    # Out of vocabulary.
                    probabilities[n] += [self.lowest_probability[n]]

        # The dictionary indexing here is hard to read.
        privacy_scores = [np.mean(probabilities[n]) for n in range(1, self.n_gram_limit + 1)]
        privacy_percent = [get_reference_score(self.reference_scores[n], privacy_scores[n-1]) for n in range(1, self.n_gram_limit + 1)]

        # pprint(text_tokens)
        # pprint(probabilities)
        # print(self.total_probability)
        # pprint(self.probability_range)
        # print(privacy_scores)
        # print(privacy_percent)

        return privacy_scores, privacy_percent, probabilities, ngram_tokens


def get_reference_score(reference, score):

    # reference = np.sort(reference)
    # print(reference)
    for idx, ref_score in enumerate(reference):
        if score < ref_score:
            # print(idx, len(reference), ref_score, score)
            return 1 - idx / len(reference)

    return 0


def get_ngrams(input_list, n):

    # From http://www.locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/

    return zip(*[input_list[i:] for i in range(n)])


if __name__ == '__main__':

    risk_evaluator = RiskEvaluator()

    # Load Data
    # Currently sourced from https://norvig.com/ngrams/
    risk_evaluator.load_dataset()

    # Evaluate sample quote
    sample_quote = "The ultimate measure of a man is not where he stands in moments of comfort and convenience, but where he stands at times of challenge and controversy."
    risk_evaluator.evaluate_quote(sample_quote)

