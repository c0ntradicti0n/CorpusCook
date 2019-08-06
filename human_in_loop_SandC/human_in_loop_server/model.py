import itertools
import operator

from allennlp.predictors.sentence_tagger import SentenceTaggerPredictor as Predictor
import attention_please_tagger


from human_in_loop_client.corpus import Corpus

def split_list_on_lambda(l, lam):
    ''' split a list of anything based on a lambda, so that the splitting element is the first of each group '''
    groups = (list(g) for k, g in itertools.groupby(l[::-1], lam))
    reversed_groups = (list(itertools.starmap(operator.add, zip(*[groups] * 2))))
    return [l[::-1] for l in reversed_groups[::-1]]


class Model:
    def __init__(self, model_path):
        self.model = Predictor.from_path(model_path)

    def predict(self, sentence):
        results = self.model.predict_json({"sentence": sentence})
        tags = list(Corpus.bioul_to_bio(results["tags"]))
        return list(zip(results["words"], tags))

