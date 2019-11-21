
from core.annotation_protocol import *

from core.model import Model
from core.proposaler import Proposaler
from core.sampler import Sampler
from core.corpus import Corpus

#import xnym_embeddings.xnym_embeddings
#import spacy_embedder.spacy_embedder
#from allennlp.predictors.sentence_tagger import SentenceTaggerPredictor as Predictor
import customCrfTagger.cCrfT

sampler = Sampler(sample_file='samples/server_samples_bin.txt')
difference_pages = None #WebPageParser(path_to_htmls='../scraping/data')
corpus_first = Corpus(path='server/corpus/first.conll3')
corpus_over = Corpus(path='server/corpus/over.conll3')


model_first = Model(model_path="server/models/model_first.tar.gz")
model_over =  Model(model_path="server/models/model_over.tar.gz")
proposaler = Proposaler(model_first, model_over)


import pprint
from helpers.color_logger import *

class AnnotationCloud(amp.AMP):
    def log_before_after(self, what, before, after):
        logging.info(what)
        logging.info(pprint.pformat(before)[:100]+" ...")
        logging.info('-->')
        logging.info(pprint.pformat(after)[:100]+" ...")

    @MakePrediction.responder
    def makeprediction(self, text):
        annotation = model_first.predict_sentence(text)
        self.log_before_after('MakePrediction', text, annotation)
        return {'annotation': annotation}

    @DeliverSample.responder
    def deliversample(self):
        text = sampler.deliver_sample()
        self.log_before_after('DeliverSample', None, text)
        return {'text': text}

    @MakeProposals.responder
    def makeproposals(self, text):
        if not text:
            text = difference_pages.next_text()
        proposals = list(proposaler.make_proposals(text))
        self.log_before_after('MakeProposals', text, proposals)
        return {'proposals': proposals}

    @ChangeProposals.responder
    def changeproposals(self, cuts, indices, delete_add):
        proposals = proposaler.change_proposals(cuts, indices)
        self.log_before_after('ChangeProposals', cuts, proposals)
        return {'proposals': proposals, 'indices': indices, 'delete_add': delete_add}

    @SaveAnnotation.responder
    def saveannotation(self, annotation, which):
        if which == "first":
            corpus_first.write_annotation(annotation)
        elif which == "over":
            corpus_over.write_annotation(annotation)
        else:
            raise ValueError("wrong value to choose the corpus")
        self.log_before_after('SaveAnnotation', annotation, None)
        return {'done': 'yes'}

    @ZeroAnnotation.responder
    def zeroannotation(self, text, which):
        if which=="first":
             corpus_first.save_zero_annotation(text)
        elif which=="over":
            corpus_over.save_zero_annotation(text)

        self.log_before_after('ZeroAnnotation', text, None)
        return {'done': 'yes'}

    @SaveComplicated.responder
    def savecomplicated(self, text):
        sampler.complicated_sample(text)
        self.log_before_after('SaveComplicated', text, None)
        return {'done': 'yes'}

    @SaveSample.responder
    def savesample(self, text):
        sampler.add_to_library(text)
        self.log_before_after('SaveSample', text, None)
        return {'done': 'yes'}




    @DeliverPage.responder
    def deliverpage(self):
        while True:
            try:
                return {'text': difference_pages.next_text()}
            except StopIteration:
                raise FileNotFoundError(
                    "No pages anymore")
            # TODO
            #  pages store empty: err callback to lead to generating more pages

def main():
    from twisted.internet import reactor
    from twisted.internet.protocol import Factory
    protofacto = Factory()
    protofacto.protocol = AnnotationCloud
    reactor.listenTCP(5180, protofacto)
    logging.info('Server started and is waiting for commands')
    reactor.run()

if __name__ == '__main__':
    main()
