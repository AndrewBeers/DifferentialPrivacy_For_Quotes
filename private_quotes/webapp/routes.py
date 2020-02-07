import os

from flask import Flask, flash, request, redirect, url_for, render_template, session, send_from_directory
from flask.json import jsonify

from private_quotes import app
from private_quotes.core.risk_evaluation import RiskEvaluator

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


risk_evaluator = RiskEvaluator()
risk_evaluator.load_dataset()


class ReusableForm(Form):
    name = TextField('Quote:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    #print(form.errors)
    if request.method == 'POST':
        quote = request.form['quote']

        privacy_scores, probabilities, ngram_tokens = risk_evaluator.evaluate_quote(quote)
        probabilities = [probabilities[n] for n in [1, 2]]
        ngram_tokens = [ngram_tokens[n] for n in [1, 2]]

        print(list(zip(ngram_tokens[0], probabilities[0])))
        unigram_outputs = [f'{str(unigram)}: {prob}' for unigram, prob in zip(ngram_tokens[0], probabilities[0])]
        unigram_outputs = ['Unigrams:'] + unigram_outputs

        bigram_outputs = [f'{str(bigram)}: {prob}' for bigram, prob in zip(ngram_tokens[1], probabilities[1])]
        bigram_outputs = ['Bigrams:'] + bigram_outputs

        print(unigram_outputs)
        print(privacy_scores)
        print(probabilities)
        print(ngram_tokens)

        if form.validate():
            flash('{}'.format(quote))
        else:
            flash([[f'Input quote: "{quote}"',
                        f'Your privacy score on unigrams is {privacy_scores[0]}.', 
                        f'Your privacy score on bigrams is {privacy_scores[1]}'],

                    unigram_outputs,
                    bigram_outputs])

    return render_template('index.html', form=form)