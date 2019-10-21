import spacy
from more_itertools import pairwise
from nltk import flatten
import regex as re

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
    def __init__(self, model_to_predict, max_len = 100):

        self.model = model_to_predict
        self.max_len = max_len
        self.annotation_scheme = bio_annotation

        self.id_source = next_natural_number()
        next(self.id_source)

    allowed_chars = sorted(""" !?$%&()+,-.\ 0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ()[]_`abcdefghijklmnopqrstuvwxyz‘’“”\n""")
    def clean(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = "".join([c for c in text if c in self.allowed_chars])
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


    def make_proposals(self, text):
        text =  self.clean(text)

        self.doc  = nlp(text)
        sent_cuts = [sp.start for sp in self.doc.sents]
        print (sent_cuts)
        start_i, end_i = self.next_proposal(self.doc, sent_cuts, start_i=0)

        while start_i != end_i:
            result = self.get_sample(start_i, end_i, self.doc[sent_cuts[start_i]:sent_cuts[end_i]])
            yield result
            last_mark = sent_cuts[start_i] + result['mark_end']
            new_start_i = sent_cuts.index(min (sent_cuts, key= lambda x: abs(last_mark-x)))
            start_i = start_i+1 if new_start_i == start_i else new_start_i
            start_i, end_i = self.next_proposal(self.doc, sent_cuts, start_i)

    def next_proposal (self, whole_doc, whole_sent_starts, start_i):
        next_i = start_i
        while next_i < len(whole_sent_starts)-1 and len(whole_doc[whole_sent_starts[start_i]:whole_sent_starts[next_i]])< self.max_len:
            next_i += 1
        return start_i, next_i

    def make_windwos(self, doc, text, cuts):
        numba, cut_i = zip(*cuts)
        groups       = list(zip(cuts, seq_split(doc, lambda t: t.i not in cut_i)))
        return groups

    def get_predicted_annotations (self, windows):
        reasonable_samples = (self.get_sample_if_reasonable(r) for r in windows)
        return [r for r in reasonable_samples if r]

    def get_sample(self, start_i, end_i, sentence_span):
        text = " ".join([t.text for t in sentence_span])
        indices = [t.i for t in sentence_span]
        if not text:
            raise ValueError("no text in given span")

        text =  self.clean(text)
        annotation = self.model.predict_sentence(text)

        tokens = [x[0] for x in annotation]
        tags = [x[1] for x in annotation]
        relevant_tags =  [x != "O" for x in tags]
        if True in relevant_tags:
            mark_end = relevant_tags[::-1].index(True) # global position of span end of annotation
        else:
            mark_end = len(tokens)
        return {
            'annotation': annotation,
            'indices': indices,
            'tokens': tokens,
            'text': text,
            'start': start_i,
            'id': next(self.id_source),
            'mark_end': mark_end,
            'difference':any(relevant_tags)
        }

    def change_proposals(self, cuts, indices):
        sentences = list(self.doc.sents)
        relevant_sentences = [sentences[s:e] for s, e in pairwise(cuts)]
        windows = list(zip(zip(cuts, indices), relevant_sentences))
        new_proposals = self.get_predicted_annotations(windows)
        return new_proposals







