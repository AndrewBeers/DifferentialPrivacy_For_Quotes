import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

from nltk.corpus import brown
from pprint import pprint
from collections import defaultdict
from tqdm import tqdm

from private_quotes.core.risk_evaluation import RiskEvaluator


def prepare_reference_probabilities():

    """ This function is 'struggle coding',
        and should be totally refactored.
    """

    risk_evaluator = RiskEvaluator()
    risk_evaluator.load_dataset()

    all_privacy_scores = defaultdict(list)
    for sent in tqdm(brown.sents()):
        privacy_scores, privacy_percents, probabilities, ngram_tokens = risk_evaluator.evaluate_quote(' '.join(sent))
        all_privacy_scores[1] += [privacy_scores[0]]
        all_privacy_scores[2] += [privacy_scores[1]]

    all_privacy_scores[1] = np.sort(all_privacy_scores[1])
    all_privacy_scores[2] = np.sort(all_privacy_scores[2])
    # pprint(all_privacy_scores[1])
    # plt.hist(all_privacy_scores[1], normed=True, bins=30)
    # plt.ylabel('Probability')
    # plt.show()

    output_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data/reference_scores.pkl')

    with open(output_filepath, 'wb') as f:
        pickle.dump(all_privacy_scores, f)

    return


if __name__ == '__main__':

    prepare_reference_probabilities()