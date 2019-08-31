from human_in_loop_SandC.human_in_loop_client.annotation_protocol import *

from human_in_loop_SandC.human_in_loop_server.model import Model
from human_in_loop_SandC.human_in_loop_server.proposaler import Proposaler
from human_in_loop_SandC.human_in_loop_server.sampler import Sampler
from human_in_loop_SandC.human_in_loop_client.corpus import Corpus
from human_in_loop_SandC.human_in_loop_server.webpageparser import WebPageParser

import xnym_embeddings.xnym_embeddings
import attention_please_tagger.attention_please_tagger
import spacy_embedder.spacy_embedder



corpus = Corpus(path='server_annotations.conll3')
sampler = Sampler(sample_file='server_samples_bin.txt')
difference_pages = WebPageParser(path_to_htmls='../scraping/data')
model = Model(model_path="human_in_loop_server/ai_models/models/model.tar.gz")
proposaler = Proposaler(model)


import pprint
from helpers.color_logger import *

class AnnotationCloud(amp.AMP):
    def log_before_after(self, what, before, after):
        logging.info(what)
        logging.info(pprint.pformat(before))
        logging.info('-->')
        logging.info(pprint.pformat(after))

    @MakePrediction.responder
    def makeprediction(self, text):
        annotation = model.predict(text)
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
        proposals = proposaler.make_proposals(text)
        self.log_before_after('MakeProposals', text, proposals)
        return {'proposals': proposals}

    @SaveAnnotation.responder
    def saveannotation(self, annotation):
        corpus.write_annotation(annotation)
        self.log_before_after('SaveAnnotation', annotation, None)
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

    @ZeroAnnotation.responder
    def zeroannotation(self, text):
        corpus.save_zero_annotation(text)
        self.log_before_after('ZeroAnnotation', text, None)
        return {'done': 'yes'}

    @DeliverPage.responder
    def deliverpage(self):
        while True:
            try:
               return {'text':difference_pages.next_text()}
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
    logging.warning('Server started, waiting for commands')
    reactor.run()

if __name__ == '__main__':
    main()