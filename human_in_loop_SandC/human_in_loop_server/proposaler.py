import itertools
from pprint import pprint
from typing import List

import spacy
from more_itertools import pairwise, split_before
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



    def make_proposals(self, text):
        text =  self.model.clean(text)

        self.doc  = nlp(text)
        sent_cuts = [sp.start for sp in self.doc.sents]
        print (sent_cuts)
        start_i, end_i = self.next_proposal(self.doc, sent_cuts, start_i=0)

        done = []
        while start_i != end_i:
            span = sent_cuts[start_i],sent_cuts[end_i]
            if span in done:
                print ("repeating work, why?")
                start_i =  end_i
                end_i = start_i + 4
            result = self.get_sample(start_i, end_i, self.doc[span[0]:span[1]], sent_cuts)
            done.append(span)

            last_start_i, last_end_i = start_i, end_i
            yield result
            last_mark = sent_cuts[start_i] + result['mark_end']
            new_start_i = sent_cuts.index(min (sent_cuts, key= lambda x: abs(last_mark-x)))
            start_i = start_i if new_start_i == start_i else new_start_i
            start_i, end_i = self.next_proposal(self.doc, sent_cuts, start_i)
            if start_i < last_end_i:
                print ("starting at tokens before")

    def next_proposal (self, whole_doc, whole_sent_starts, start_i):
        """ Effectively this functions computes the new end of the span, that fits in the window of text to be analysed

        :param whole_doc:
        :param whole_sent_starts:
        :param start_i:
        :return:
        """
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

    def get_sample(self, start_i, end_i, sentence_span,  sentence_cuts, depth = 0, max_depth = 1):
        """ make the prediction based on some parts of the text, optionally regarding also distinctions, that appear
        within the sides or arms of a found distinction

        :param start_i:
        :param end_i:
        :param sentence_span:
        :param sentence_cuts:
        :param depth:
        :param max_depth:
        :return:
        """
        text = " ".join([t.text for t in sentence_span])
        indices = [t.i for t in sentence_span]
        if not text:
            raise ValueError("no text in given span")

        text =  self.model.clean(text)
        annotation = self.model.predict_sentence(text)

        tokens = [x[0] for x in annotation]
        tags = [x[1] for x in annotation]
        relevant_tags =  [x != "O" for x in tags]
        beginning_tags =  [x for x in tags if x[0] == 'B']

        number_of_annotations = [t[0] for t in tags].count('B')

        annotation_groups = list(split_before(zip(indices, tags), lambda x: x[1][0] == 'B'))

        pprint (annotation_groups)
        subs = []
        if True in relevant_tags and depth < max_depth:
            # global position of span end of annotation
            mark_end = len(relevant_tags) - relevant_tags[::-1].index(True)  # last tags (look backwards and index first True and thats the position from the end

            if number_of_annotations>=2:
                # positions of group starts until end
                middles = set([sentence_cuts[Proposaler.nearest(b[0][0], sentence_cuts, before=True)] for b in annotation_groups] +
                              [indices[-1]+2])
                # approximate closest sentence borders before each annotation
                # make new predictions for sides of distinctions
                print ([(group[0][0], group[-1][0])
                         for group in annotation_groups])
                try:
                    subs = [
                        self.get_sample(
                            start_i       = group[0][0],
                            end_i         = group[-1][0],
                            sentence_span = self.doc[group[0][0]: group[-1][0]],
                            sentence_cuts = sentence_cuts,
                            depth         = depth+1,
                            max_depth     = max_depth
                         ) for group in annotation_groups]
                    print (subs)
                    mark_end = max([mark_end, *[s['mark_end'] for s in subs]])
                except Exception as e:
                    print (str(e))
                subs = [s for s in subs if s['difference']]

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
            'annotated': any(relevant_tags),
            'difference': number_of_annotations >=2 ,
            'subs': subs
        }

    def change_proposals(self, cuts, indices):
        sentences = list(self.doc.sents)
        relevant_sentences = [sentences[s:e] for s, e in pairwise(cuts)]
        windows = list(zip(zip(cuts, indices), relevant_sentences))
        new_proposals = self.get_predicted_annotations(windows)
        return new_proposals

    def nearest(position:int, positions:List[int], before: bool = False, after: bool = False) -> int:
        """ Approximating the index, that is next to some value of a specified list, the index can be specified
        to be before or after this matched element.

        At beginning
        >>> Proposaler.nearest (6, [3,8,12])
        1
        >>> Proposaler.nearest (6, [3,8,12], before=True)
        0
        >>> Proposaler.nearest (4, [3,8,12], after=True)
        1

        More at the end
        >>> Proposaler.nearest (42, [3, 8, 12, 43, 100])
        3
        >>> Proposaler.nearest (99, [3, 8, 12, 43, 100], before=True)
        3
        >>> Proposaler.nearest (44, [3, 8, 12, 43, 100], after=True)
        4

        Borders of range
        >>> Proposaler.nearest (100, [3, 8, 12, 43, 100])
        4
        >>> Proposaler.nearest (3, [3, 8, 12, 43, 100])
        0
        >>> Proposaler.nearest (100, [3, 8, 12, 43, 100], before=True)
        4
        >>> Proposaler.nearest (3, [3, 8, 12, 43, 100], before=True)
        0
        >>> Proposaler.nearest (100, [3, 8, 12, 43, 100], after=True)
        4
        >>> Proposaler.nearest (3, [3, 8, 12, 43, 100], after=True)
        0

        Out out range

        >>> Proposaler.nearest (300, [3, 8, 12, 43, 100])
        4
        >>> Proposaler.nearest (2, [3, 8, 12, 43, 100])
        0
        >>> Proposaler.nearest (500, [3, 8, 12, 43, 100], before=True)
        4
        >>> Proposaler.nearest (1, [3, 8, 12, 43, 100], after=True)
        0


        :param position:
        :param positions:
        :param before:
        :param after:
        :return:
        """
        pos = positions.index(min(positions, key=lambda x: abs(position - x)))

        if before:
            if position < min(positions):
                raise ValueError("Before can't before all, if looking before")
            elif position < positions[pos]:
                return pos - 1
            else:
                return pos
        elif after:
            if position > max(positions):
                raise ValueError("After can't be after after all")
            elif position > positions[pos]:
                return pos + 1
            else:
                return pos
        else:
            return pos

