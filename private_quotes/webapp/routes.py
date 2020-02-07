import os

from flask import Flask, flash, request, redirect, url_for, render_template, session, send_from_directory, Markup
from flask.json import jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from colour import Color

from private_quotes import app
from private_quotes.core.risk_evaluation import RiskEvaluator


risk_evaluator = RiskEvaluator()
risk_evaluator.load_dataset()
color_spectrum = list(Color("red").range_to(Color("green"), 20))
hex_spectrum = [color.get_hex() for color in color_spectrum]
# <span style="background-color:#00FEFE">Cyan Text</span>
# -3 to -19 

class ReusableForm(Form):
    name = TextField('Quote:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    #print(form.errors)
    if request.method == 'POST':
        quote = request.form['quote']

        privacy_scores, privacy_percents, probabilities, ngram_tokens = risk_evaluator.evaluate_quote(quote)
        probabilities = [probabilities[n] for n in [1, 2]]
        ngram_tokens = [ngram_tokens[n] for n in [1, 2]]

        print(list(zip(ngram_tokens[0], probabilities[0])))
        unigram_outputs = [f'{str(unigram)}: {round(prob, 2)}' for unigram, prob in zip(ngram_tokens[0], probabilities[0])]
        unigram_outputs = ['Unigrams:'] + unigram_outputs
        
        colored_unigrams = [Markup(f'<span style="background-color:{hex_spectrum[int(prob + 19)]}">{unigram[0]}</span>') for unigram, prob in zip(ngram_tokens[0], probabilities[0])]
        print(colored_unigrams)

        bigram_outputs = [f'{str(bigram)}: {round(prob, 2)}' for bigram, prob in zip(ngram_tokens[1], probabilities[1])]
        bigram_outputs = ['Bigrams:'] + bigram_outputs

        # Revisit this and make it not.. inscrutable.
        bigram_probabilities = [probabilities[1][0]] + probabilities[1] + [probabilities[1][-1]]
        bigram_probabilities = [(bigram_probabilities[i] + bigram_probabilities[i + 1]) / 2 for i in range(len(bigram_probabilities) - 1)]
        colored_bigrams = [Markup(f'<span style="background-color:{hex_spectrum[int(prob + 19)]}">{unigram[0]}</span>') for unigram, prob in zip(ngram_tokens[0], bigram_probabilities)]
        print(colored_bigrams)

        print(unigram_outputs)
        print(privacy_scores)
        print(probabilities)
        print(ngram_tokens)

        if form.validate():
            flash('{}'.format(quote))
        else:
            flash([[f'Input quote: "{quote}"',
                        f'Your privacy score on unigrams is {round(privacy_scores[0], 2)}, which is in the {round(privacy_percents[0] * 100, 0)}th percentile for uniqueness.',
                        f'Your privacy score on bigrams is {round(privacy_scores[1], 2)}, which is in the {round(privacy_percents[1] * 100, 0)}th percentile for uniqueness.'],

                    colored_unigrams,
                    colored_bigrams,
                    unigram_outputs,
                    bigram_outputs])

    return render_template('index.html', form=form)