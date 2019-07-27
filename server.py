import json
import pprint

import sys
import traceback

from human_in_loop.corpus import Corpus
from human_in_loop.model import Model
from human_in_loop.sampler import Sampler
from helpers.color_logger import *

model = Model(model_path="models/model.tar.gz")
corpus = Corpus(path='hil19.conll3')
sampler = Sampler(sample_file='server_samples_bin.txt')

import regex as re

routing_protocol_client_to_server = {
    'make_prediction':
        {'fun': lambda x: model.predict(x['text']),
         'answer': 'prediction'
        },
    'deliver_sample':
        {'fun': lambda x: sampler.deliver_sample(),
         'answer': 'got_sample',
         'except': 'make_new_samples'
         },
    'save_sample':
        {'fun': lambda x: sampler.add_to_library(x['text'])},
    'save_a_complicated_sample':
        {'fun': lambda x: sampler.complicated_sample(x['text'])},
    'save_annotation':
        {'fun': lambda x: corpus.write_sample(annotation=x['annotation'])},
    'could_you_train?':
        {'fun': lambda x: model.train()}
}


# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""


    def dataReceived(self, data):
        if not isinstance(data, str):
            data = data.decode('utf-8')
        logging.info ('command was: %s' % (pprint.pformat(data)))
        if '}{' in str(data):
            logging.warning('double command!')
            commands = re.findall(r'({[^{}]+})', str(data))
            for c in commands:
                self.dataReceived(c)
            return
        try:
            json_msg = json.loads(data)
        except json.decoder.JSONDecodeError:
            logging.error('not a valid command, ignoring')
            return

        logging.info (" ".join(['Is this a json-value?', str('command' in json_msg)]))

        if 'command' in json_msg and json_msg['command'] in routing_protocol_client_to_server:
            try:
                result = routing_protocol_client_to_server[json_msg['command']]['fun'](json_msg)
            except Exception as e:
                result = traceback.format_exc() + '\n\n\n BUT SERVER CONTINUES'
            logging.info(print (result))

            if 'except' in routing_protocol_client_to_server[json_msg['command']]:
                if not result:
                    result = {
                        'command': routing_protocol_client_to_server[json_msg['command']]['except'],
                    }


            if 'answer' in routing_protocol_client_to_server[json_msg['command']]:
                result = {
                    'command': routing_protocol_client_to_server[json_msg['command']]['answer'],
                    'result': result
                }
        else:
            result = {
                'error': 'command not in command list:\n%s' % (pprint.pformat(routing_protocol_client_to_server)),
            }

        self.transport.write(json.dumps(result).encode('utf-8'))


def main():
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(1080, factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()