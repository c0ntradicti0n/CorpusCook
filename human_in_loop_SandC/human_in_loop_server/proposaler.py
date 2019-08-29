import logging

import spacy

from human_in_loop_SandC.human_in_loop_server import bio_annotation

nlp = spacy.load("en_core_sci_sm")

def next_natural_number():
    i = 0
    while True:
        yield i
        i += 1

class Proposaler:
    def __init__(self, model_to_predict):
        self.model = model_to_predict
        self.annotation_scheme = bio_annotation

        self.id_source = next_natural_number()
        next(self.id_source)

    def make_proposals(self, text):
        doc = nlp(text)
        sentences = list(doc.sents)
        windows = self.make_windwos(doc, text)
        reasonable_samples = [self.get_sample_if_reasonable(sentences[start:stop]) for start, stop in windows]
        reasonable_samples = [r for r in reasonable_samples if r]
        return reasonable_samples

    def make_windwos(self, sentences, text):
        n_sentences = len(sentences)
        l = 5
        windows = [(i, i+l) for i in range(n_sentences-l)]
        return windows

    def get_sample_if_reasonable(self, sents_span):
        test_sample = " ".join([s.text for s in sents_span])
        if not test_sample:
            return None

        try:
            annotation = self.model.predict(test_sample)
        except ValueError:
            logging.error('models window too short.')
            return self.get_sample_if_reasonable(self, sents_span[:len(sents_span-1)])

        tokens = [x[0] for x in annotation]
        if self.annotation_scheme.BIO_Annotation.validity_check(annotation):
            return {'annotation': annotation,
                    'tokens': tokens,
                    'text': test_sample,
                    'id': next(self.id_source)}
        else:
            return None





