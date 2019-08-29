import base64
import logging
import zlib

from twisted.protocols import amp
from twisted.protocols.amp import Argument

import json
class JSON(Argument):
    """ Transfrom json to byte string and retransform it back """
    def toString(self, inObject):
        return json.dumps(inObject, ensure_ascii=False).encode('utf-8')

    def fromString(self, inString):
        return json.loads(inString.decode('utf-8'))

class JSONB64COMPRESS(Argument):
    """ Transfrom json to byte string and retransform it back """
    def toString(self, inObject):
        l_before = len(json.dumps(inObject).encode('ascii'))
        l_after = len(base64.b64encode(
            zlib.compress(
                json.dumps(inObject).encode('ascii')
            )
        ).decode('utf-8'))

        logging.error('compression: %d to %d, means to %2.1f%% of the original' % (l_before, l_after, 100/(l_before/l_after)))

        return base64.b64encode(
            zlib.compress(
                str(json.dumps(inObject)).encode('ascii')
            )
        )

    def fromString(self, inString):
        return json.loads(zlib.decompress(base64.b64decode(inString)))

class DeliverPage(amp.Command):
    arguments = []
    response = [(b'text', amp.Unicode())]


class MakePrediction(amp.Command):
    arguments = [(b'text', amp.Unicode())]
    response = [(b'annotation', JSON())]


class DeliverSample(amp.Command):
    arguments = []
    response = [(b'text', amp.Unicode())]

class MakeProposals(amp.Command):
    arguments = [(b'text', amp.Unicode())]
    response = [(b'proposals', JSONB64COMPRESS())]


class SaveAnnotation(amp.Command):
    arguments = [(b'annotation', JSON())]
    response =  [(b'done', amp.Unicode())]


class SaveComplicated(amp.Command):
    arguments = [(b'text', amp.Unicode())]
    response =  [(b'done', amp.Unicode())]


class SaveSample(amp.Command):
    arguments = [(b'text', amp.Unicode())]
    response =  [(b'done', amp.Unicode())]


class ZeroAnnotation(amp.Command):
    arguments = [(b'text', amp.Unicode())]
    response =  [(b'done', amp.Unicode())]
