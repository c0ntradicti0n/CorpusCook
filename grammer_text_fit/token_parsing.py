import coloredlogs
coloredlogs.install()
import logging
logging.getLogger().setLevel(logging.INFO)

from grammer_text_fit.tok import Tok
from helpers import nested_dict_tools
from typing import Iterable

import spacy
from spacy.tokenizer import Tokenizer
from spacy.matcher import PhraseMatcher
#import neuralcoref

nlp = spacy.load("en_core_web_lg")
#neuralcoref.add_to_pipe(nlp, greedyness=0.575)
tokenizer = Tokenizer(nlp.vocab)
matcher = PhraseMatcher(nlp.vocab)

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

matching_functions = []
@parametrized
def matching_function(func, vocab):
    global matching_functions
    vocab = [[t.lemma_ for t in nlp(phrase)] for phrase in vocab  ]
    func.vocab = vocab
    matching_functions.append(func)
    return func


def get_this(token, attribute):
    if isinstance(getattr(token, attribute), Iterable) and not isinstance(getattr(token, attribute), str) :
        return list(getattr(token, attribute))
    else:
        return getattr(token, attribute)

def prepare_text(text_s):
    ''' this calls preprocessing methods recursively on a nested data structure or just a string

    :param text_s: string or iterable structure with strings
    :return: the same type, but tokenized instead of strings

    '''
    if isinstance(text_s, str):
        return prepare_single_token(text_s)
    else:
        return nested_dict_tools.apply(text_s, prepare_single_token)


attributes = ['text', 'dep_', 'pos_', 'tag_', 'lemma_', 'i', 'subtree']
def prepare_single_token(text):
    if not text:
        return None

    doc = nlp(text)
    tokens = [Tok({'spacy':t, **{a: get_this(t, a) for a in attributes}}) for t in doc if t.pos_ != 'SPACE' and t]
    return tokens


def prepare_labels( distinction_patterns):
    repaired_distinctions = repair_distinctions(distinction_patterns)
    annotated_labels =[
        tuple(
            {
                k: prepare_single_token(v.replace('.',',').replace('-', ''))
                if v else v # Keep None
                for k, v in nested_dict_tools.nested_dict_iter(dist)
            }
            for dist in dists
        )
        for dists in repaired_distinctions
    ]
    return annotated_labels

just_positive = ['yes', 'true']
just_negative = ['no', 'false', '', 'none']
just_between = ['maybe']
just_positive_negative = just_positive + just_negative + just_between

def repair_distinctions(patterns):
    try:
        for d in patterns:
            for s in d:
                for k,v in s.items():
                    if isinstance(v, list):
                        s[k]=" ".join(v).lower()

            try:
                any(s['contrast'].lower() in just_positive_negative for s in d)
            except TypeError:
                raise ValueError("annotation pattern entry can't be a string, must be a dict")

            if any(s['contrast'].lower() in just_positive_negative for s in d):
                for s in d:
                    if s['contrast'] in just_negative:
                        s['contrast'] = " ".join(['not', s['aspect']])
                    if s['contrast'] in just_positive:
                        s['contrast'] = " ".join(['', s['aspect']])
                    if s['contrast'] in just_between:
                        s['contrast'] = " ".join(['maybe', s['aspect']])

            if all(s['aspect'] == None for s in d):
                continue

            if any(s['aspect'].lower() in just_positive_negative for s in d):
                for s in d:
                    s['aspect'] = None

            if s['aspect']==None or s['aspect'].lower() == 'no_aspect':
                for s in d:
                    s['aspect'] = None

    except KeyError:
        logging.warning('no subject/contrast/aspect key in match dict')
        pass
    return patterns
