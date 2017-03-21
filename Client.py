# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.username
        self.host = host
        self.server_port = server_port
        self.run()
        self.receive_message(self, self.connection)

        self.holdMessage
        self.messageDict

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        
    def disconnect(self):
        
        self.connection.close()
        exit()

    def receive_message(self, message):
        
        self.messageDict = self.MessageParser().parse_message(self, message)

    def send_payload(self, data):
        if data == 'help':
            dataDict = {'request':'help', 'conten': ''}
        elif data == 'names':
            dataDict = {'request':'names', 'content': ''}
        elif data == 'logout':
            dataDict = {'request':'logout', 'content': ''}
        else:
            if not self.loggedIn:
                dataDict = {'request':'login', 'content': data}
            else:
                dataDict = {'request':'msg', 'content': data}

        self.connection.send(json.dumps(dataDict))


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('192.168.1.98', 9998)
