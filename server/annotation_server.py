from core.annotation_protocol import *
import customCrfTagger.cCrfT
from core.model import Model
from core.textsplitter import TextSplitter
from core.sampler import Sampler
from core.corpus import Corpus
from server.core.annotation_protocol import Ping
from server.core.auto_corpus import AutoCorpus

sampler = Sampler(sample_file='samples/server_samples_bin.txt')
corpus_first = Corpus(path='server/corpus/first.conll3')
corpus_over = Corpus(path='server/corpus/over.conll3')
corpus_auto_first = Corpus(path='manually_annotated/topics/auto_first.conll3')

#auto_corpus_second = AutoCorpus(which="over", corpus_over)
model_first = Model(model_path="server/models/model_first.tar.gz")
#model_over =  Model(model_path="server/models/model_over.tar.gz")
textsplitter = TextSplitter(model_first, None)

from helpers.color_logger import *

class AnnotationCloud(amp.AMP):
    def log_before_after(self, what, before, after):
        logging.info(what)
        logging.info(f"{str(before[:100])} \n... -->\n{str(after[:100])} ...")

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
    def makeproposals(self, text, text_name):
        proposals = list(textsplitter.make_proposals(text))
        self.log_before_after(f"Maked proposals for {text_name}", text, proposals[2])
        return {'proposals': proposals}

    @MakeProposalsIndexed.responder
    def makeproposalsindexed(self, indexed, text_name):
        proposals = list(textsplitter.make_proposals(indexed))

        self.log_before_after('MakeProposals', indexed, proposals)
        return {'proposals': proposals}

    @ChangeProposals.responder
    def changeproposals(self, cuts, indices, delete_add):
        proposals = textsplitter.change_proposals(cuts, indices)
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



    """
    @DeliverPage.responder
    def deliverpage(self):
        while True:
            try:
                return {'text': difference_pages.next_text()}
            except StopIteration:
                raise FileNotFoundError(
                    "No pages anymore")
            # TODO
            #  pages store empty: error callback to lead to generating more pages
    """

    @Ping.responder
    def ping(self, text):
        logging.info("ping received!")
        return {'done': 'yes'}


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
