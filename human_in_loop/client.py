# install_twisted_rector must be called before importing the reactor
from __future__ import unicode_literals

import json
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
         }
    }



class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.client.on_connection(self.transport)

    def dataReceived(self, data):
        print(data)
        commands = re.findall(r'({[^{}]+}|"None")', str(data))
        for c in commands:
            self.evaluate(c)
        return

    def evaluate(self, data):
        try:
            json_msg = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            print (data)
            raise e



        if json_msg is None:
            return

        #print ("That was the message: ", json_msg)
        #print ('command' in json_msg)
        #print ('command' in json_msg and json_msg['command'] in routing_protocol_server_to_client)

        if 'command' in json_msg and json_msg['command'] in routing_protocol_server_to_client:
            #print ('client received valid json command')
            try:
                routing_protocol_server_to_client[json_msg['command']]['fun'](self.factory.app, json_msg['result'])
            except Exception as e:
                routing_protocol_server_to_client[json_msg['command']]['except'](self.factory.app)
                print(str(e) + "\n\n\nERRONEOUS COMMAND FROM SERVER, NEGLECTING")
            #print ('client did valid json command')
        #self.factory.client.print_message(data.decode('utf-8'))


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
        print (json.dumps(command))
        self.send_message(msg=json.dumps(command))

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, EchoClientFactory(app=self.app, client=self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def send_message(self, *args, msg=''):
        if msg and self.connection:
            self.connection.write(msg.encode('utf-8'))

    def print_message(self, msg):
        print (msg)

