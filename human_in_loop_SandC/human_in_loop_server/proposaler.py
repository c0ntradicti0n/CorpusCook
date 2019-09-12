import logging
import pprint
from itertools import groupby

import spacy
from more_itertools import pairwise
from nltk import flatten

nlp = spacy.load("en_core_sci_sm")

from human_in_loop_SandC.human_in_loop_server import bio_annotation


def next_natural_number():
    i = 0
    while True:
        yield i
        i += 1

def seq_split(lst, cond):
    sublst = [lst[0]]
    for item in lst[1:]:
        if cond(item):
            sublst.append(item)
        else:
            yield sublst
            sublst = [item]
    if sublst:
        yield sublst


def approx_unique(urn=[], choices=[], variance=0.005):
    d = round(max(flatten([urn]+choices)) * variance)
    for i, v in enumerate(urn):
        if any(vd in flatten(choices) for vd in range(v-d, v+d)):
            yield i, v

class Proposaler:
    def __init__(self, model_to_predict):
        self.model = model_to_predict
        self.annotation_scheme = bio_annotation

        self.id_source = next_natural_number()
        next(self.id_source)

    def make_proposals(self, text):
        self.doc  = nlp(text)
        sent_cuts = [sp.start for sp in self.doc.sents]
        nl_cuts   = [t.i+1 for t in self.doc if t.text=="\n"]
        cuts      = list(approx_unique(urn=sent_cuts, choices=nl_cuts))
        windows   = self.make_windwos(self.doc, text, cuts)
        predicted =  self.get_predicted_annotations(windows)
        return predicted

    def make_windwos(self, doc, text, cuts):
        numba, cut_i = zip(*cuts)
        groups       = list(zip(cuts, seq_split(doc, lambda t: t.i not in cut_i)))
        return groups

    def get_predicted_annotations (self, windows):
        reasonable_samples = (self.get_sample_if_reasonable(r) for r in windows)
        return [r for r in reasonable_samples if r]

    def get_sample_if_reasonable(self, cutted_sentence_span):
        (cut_i, cut_toki), sentence_span = cutted_sentence_span
        text = " ".join([s.text for s in sentence_span])
        if not text:
            return None
        try:
            annotation = self.model.predict(text)
        except ValueError:
            logging.error('models window too short.')
            logging.error('%s' % (str(sentence_span)))
            return None

        tokens = [x[0] for x in annotation]
        if True or self.annotation_scheme.BIO_Annotation.validity_check(annotation):
            return {'annotation': annotation,
                    'tokens': tokens,
                    'text': text,
                    'cut': cut_i,
                    'id': next(self.id_source)}
        else:
            return None

    def change_proposals(self, cuts, indices):
        sentences = list(self.doc.sents)
        relevant_sentences = [sentences[s:e] for s, e in pairwise(cuts)]
        windows = list(zip(zip(cuts, indices), relevant_sentences))
        new_proposals = self.get_predicted_annotations(windows)
        return new_proposals







