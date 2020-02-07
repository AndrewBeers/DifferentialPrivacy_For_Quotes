import numpy as np
import pickle

from random import randint


def calc_privacy_cost(input_string, n_gram_transitions):

    n_grams = partition_into_ngrams(input_string)

    privacy_cost = 0
    for n_gram in n_grams:
        n_gram = tuple(n_gram)
        try:
            privacy_cost += (1 / n_gram_transitions[n_gram])
        except:
            pass

    return privacy_cost


def generate_sentence_alteration(input_quote):

    input_quote[randint(len(input_quote))] = select_random_word()

    return input_quote


def select_random_word():

    return 'hammer'


def partition_into_n_grams():

    return

    


if __name__ == '__main__':

    # Dummy dataset
    n_gram_transitions = {('lazy', 'dumbledore'): 0.0001, ('dog', 'jumped'): 0.1}
    # n_gram_transitions = pickle.load('fanfiction_transitions.npy')

    privacy_tolerance = 0.1
    input_quote = "The quick brown dog jumped over the lazy Dumbledore."
    privacy_cost = calc_privacy_cost(input_quote, n_gram_transitions)
    new_quote = input_quote

    while privacy_cost > privacy_tolerance:
        new_quote = generate_sentence_alteration(new_quote)
        privacy_cost = calc_privacy_cost(new_quote, n_gram_transitions)

    print('A tolerable privacy tolerance has been achieved') 