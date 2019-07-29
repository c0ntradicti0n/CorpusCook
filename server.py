from human_in_loop_client.annotation_protocol import *

from human_in_loop_server.model import Model
from human_in_loop_server.sampler import Sampler
from human_in_loop_client.corpus import Corpus

model = Model(model_path="models/model.tar.gz")
corpus = Corpus(path='server_annotations.conll3')
sampler = Sampler(sample_file='server_samples_bin.txt')
difference_pages = sampler.next_page()

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

    @SaveAnnotation.responder
    def saveannotation(self, annotation):
        corpus.write_sample(annotation)
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

    @DeliverPage.responder
    def deliverpage(self):
        while True:
            try:
               return {'text':next(difference_pages)['difference_text'].replace('\n',' ').replace('  ', ' ')}
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
    reactor.listenTCP(1080, protofacto)
    logging.warning('Server started, waiting for commands')
    reactor.run()

if __name__ == '__main__':
    main()