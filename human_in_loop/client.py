# install_twisted_rector must be called before importing the reactor
from __future__ import unicode_literals

import json
import pprint
import traceback
from helpers.color_logger import *

import regex as re
from kivy.support import install_twisted_reactor

install_twisted_reactor()

# A Simple Client that send messages to the Echo Server
from twisted.internet import reactor, protocol

routing_protocol_server_to_client = {
    'prediction': {
         'fun':  lambda app, annotation: app.take_next_rest(annotation),
         'except':
                 lambda app: app.take_next()
         },
    'got_sample': {
        'fun':  lambda app, annotation: app.got_sample(annotation),
        'except':
            lambda app: app.take_next()
    }
}



class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.client.on_connection(self.transport)

    def dataReceived(self, data):
        data = data.decode('utf-8')
        print (type(data))
        print(data)
        commands = re.findall(r'({[^{}]+}|"None")', str(data))
        for c in commands:
            self.evaluate(c)
        return

    def evaluate(self, data):
        try:
            json_msg = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            logging.error(data)
            raise e

        if json_msg is None:
            return

        if 'command' in json_msg and json_msg['command'] in routing_protocol_server_to_client:
            try:
                routing_protocol_server_to_client[json_msg['command']]['fun'](self.factory.app, json_msg['result'])
            except Exception as e:
                result = pprint.pformat(traceback.format_exc()) + '\n\n\n But client continues'
                logging.debug(result)
                raise
                routing_protocol_server_to_client[json_msg['command']]['except'](self.factory.app)
        else:
            logging.error('Not a valid answer from the server; no command or command not in routing_protocol_server_to_client %s'
                   % pprint.pformat(data))


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app, client):
        self.app = app
        self.client = client

    def startedConnecting(self, connector):
        self.client.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        self.client.print_message('Lost connection.')

    def clientConnectionFailed(self, connector, reason):
        self.client.print_message('Connection failed.')



class Client:
    connection = None

    def __init__(self, app):
        self.app = app

        self.connect_to_server()

    def commander(self, command='--help?', **kwargs):
        command = {
            'command':command,
            **kwargs
        }
        logging.debug(json.dumps(command))
        self.send_message(msg=json.dumps(command))

    def connect_to_server(self):
        reactor.connectTCP('134.76.20.154', 80, EchoClientFactory(app=self.app, client=self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def send_message(self, *args, msg=''):
        if msg and self.connection:
            self.connection.write(msg.encode('utf-8'))

    def print_message(self, msg):
        logging.info(msg)

