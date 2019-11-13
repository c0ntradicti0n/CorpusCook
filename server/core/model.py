import builtins
import hashlib
import itertools
import logging
import operator
import os

#from allennlp.data.tokenizers.spacy_tokenizer import SpacyTokenizer
from allennlp.data.tokenizers.word_splitter import WhitespaceTokenizer, JustSpacesWordSplitter
from regex import regex as re
from helpers.list_tools import threewise
from server.core.allennlp_predictor import SentenceTaggerPredictor as Predictor
from server.core.corpus import Corpus

def split_list_on_lambda(l, lam):
    ''' split a list of anything based on a lambda, so that the splitting element is the first of each group '''
    groups = (list(g) for k, g in itertools.groupby(l[::-1], lam))
    reversed_groups = (list(itertools.starmap(operator.add, zip(*[groups] * 2))))
    return [l[::-1] for l in reversed_groups[::-1]]

import pickle

class Model:
    def __init__(self, model_path):
        self.model = Predictor.from_path(model_path)
        self.model._tokenizer = JustSpacesWordSplitter() #SpacyTokenizer(split_on_spaces=True)

    allowed_chars = sorted(
        """ !?$%&()+,-.\ 0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ()[]_`abcdefghijklmnopqrstuvwxyz‘’“”\n""")

    def clean(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = "".join([c for c in text if c in self.allowed_chars])
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def predict_sentence(self, sentence: str):
        sentence = self.clean(sentence)
        print ("SENTENCE", sentence)
        hash = pickle.dumps(sentence)
        path = "../cache/predictions/" + hashlib.md5(str(hash).encode('utf-8')).hexdigest() + ".dump"
        if os.path.isfile(str(path)):
            with open(path, 'rb') as config_dictionary_file:
                return pickle.load(config_dictionary_file)
        else:
            try:
                results = self.model.predict_json({"sentence": sentence})
            except builtins.KeyError:
                logging.error('"%s" could not be annotated' % sentence)
                return []
            except IndexError:
                return []

            tags =   list(Corpus.bioul_to_bio(results["tags"]))
            tags =   self.clean_intermediate_beginnings(tags)
            result = list(zip(results["words"], tags))
            # Step 2
            with open(path, 'wb') as f:
                # Step 3
                pickle.dump(result, f)

            return result

    def clean_intermediate_beginnings(self, tags):
        for (i1, t1), (i2, t2), (i3, t3) in threewise(enumerate(tags)):
            if t1[0] == 'I' and t2[0]=='B' and t3[0]=='I':
                tags[i2] = 'I' + tags[i2][1:]
        return tags

