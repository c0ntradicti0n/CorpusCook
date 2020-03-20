from flask import Flask, request

import config

app = Flask(__name__)

from server.core.model import Model
from server.core.textsplitter import TextSplitter
from server.core.sampler import Sampler
from server.core.corpus import Corpus

sampler = Sampler(sample_file='samples/server_samples_bin.txt')
corpus_first = Corpus(path='server/corpus/first.conll3')
corpus_auto_first = Corpus(path='manually_annotated/topics/auto_first.conll3')
model_first = Model(model_path="server/models/model_first.tar.gz")

textsplitter = TextSplitter(model_first, None)


@app.route("/MakePrediction", methods=['POST'])
def makeprediction():
    text = request.json['text']
    annotation = model_first.predict_sentence(text)
    return {'annotation': annotation,
            'tokens':annotation}


@app.route("/DeliverSample", methods=['POST'])
def deliversample():
    text = sampler.deliver_sample()
    return {'text': text}


@app.route("/MakeProposals", methods=['POST'])
def makeproposals():
    text = request.json['text']
    text_name = request.json['text_name']
    proposals = list(textsplitter.make_proposals(text))
    return {'proposals': proposals}


@app.route("/MakeProposalsIndexed", methods=['POST'])
def makeproposalsindexed():
    indexed = request.json['indexed']
    proposals = list(textsplitter.make_proposals(tokens=list(indexed.values())))
    return {'proposals': proposals}


@app.route("/ChangeProposals", methods=['POST'])
def changeproposals():
    indices = request.json['indices']
    delete_add = request.json['delete_add']
    cuts = request.json['cuts']

    proposals = textsplitter.change_proposals(cuts, indices)
    return {'proposals': proposals, 'indices': indices, 'delete_add': delete_add}

@app.route("/SaveAnnotation", methods=['POST'])
def saveannotation():
    annotation = request.json['annotation']
    corpus_first.write_annotation(annotation)
    return True

@app.route("/ZeroAnnotation", methods=['POST'])
def zeroannotation():
    text = request.json['text']
    corpus_first.save_zero_annotation(text)
    return True

@app.route("/SaveComplicated", methods=['POST'])
def savecomplicated():
    text = request.json['text']
    sampler.complicated_sample(text)
    return True


@app.route("/SaveSample", methods=['POST'])
def savesample():
    text = request.json['text']
    sampler.add_to_library(text)
    return True


@app.route("/Ping", methods=['POST'])
def ping():
    return True


if __name__ == '__main__':
    app.debug = True
    app.url_map.strict_slashes = False
    app.run(port=config.annotation_port, debug=True, use_reloader=False)
