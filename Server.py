# -*- coding: utf-8 -*-
import socketserver
import json
import datetime
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

clients = []
usernames = []
messages = []


class ClientHandler(socketserver.BaseRequestHandler):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	username = ""
	loggedIn = False

	def handle(self):
		"""
		This method handles the connection between a client and the server.
		"""
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request

		usernameRestrictions = "Signs available for username is: a-z, A-Z, 0-9"
		helpTextLoggedIn = "Possible requests: login, logout, msg, names, help"
		helpTextNotLoggedIn = "Possible requests: login, names, help"

        # Loop that listens for messages from the client
		while True:
			received_string = self.connection.recv(4096)
            #Decode JSON and make object:
			received = json.loads(received_string)
			request = received['request']

			if request == 'login':
				login(received)
			elif request == 'logout':
				logout()
			elif request == 'msg':
				msg(received)
			elif request == 'names':
				sendInfo(user, usernames)
			elif request == 'help':
				help()
			else :
				self.connection.send(request, " is not a request")
			

	def login(received):
		tryUsername = received['content']
		if tryUsername in usernames:
			errorMessage = "Username ", tryUsername, " taken"
			self.sendError(self, errorMessage)
		elif self.loggedIn == true:
			self.sendError(self, "You are already logged in")
		elif re.match("^[A-Za-z0-9]*&", tryUsername):
			self.sendError(self, usernameRestrictions)
		else:
			self.username = tryUsername
			self.loggedIn = true
			print ("User ", self.username, " logged in")
			self.sendInfo("Logged in succsessful!")
			self.sendHistory()

	def logout():
		self.loggedIn = false
		usernames.remove(username)

	def sendMsg(received):

		if client.loggedIn:
			messageJson = self.createMessage(received['content'])

			for client in clients:
				client.connection.send(messageJson)  

	def help():

		if self.loggedIn:
			self.connection.send(helpTextLoggedIn)
		else:
			self.connection.send(helpTextNotLoggedIn)
	
	def sendError(self, message):

		timestamp = getTimestamp
		errorDict = {'timestamp': timestamp, "sender": 'server', 'response': 'error', 'content': message}
		errorJson = json.dumps(errorDict)
		self.connection.send(errorJson)

	def sendInfo(self, message):

		timestamp = getTimestamp
		infoDict = {'timestamp': timestamp, 'sender': 'server', 'response': 'info', 'content': message}
		infoJson = json.dumps(infoDict)
		self.connection.send(infoJson)

	def createMessage(self, message):

		timestamp = getTimestamp
		messageDict = {'timestamp': timestamp, "sender": self.username, 'response': 'message', 'content': message}
		messageJson = json.dumps(messageDict)
		return messageJson

	def sendHistory():

		timestamp = getTimestamp
		historyDict = {'timestamp': timestamp, 'sender': 'server', 'response': 'history','content':messages}
		historyJson = json.dumps(historyDict)
		self.connection.send(historyJson)

	def getTimestamp():

		return datetime.datetime.now().time()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
