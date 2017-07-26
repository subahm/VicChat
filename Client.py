import socket
import sys
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time


class Client(QObject):
	messageSignal = pyqtSignal(str)
	errorSignal = pyqtSignal()
	roomListSignal = pyqtSignal(str)
	z = None
	s = socket.socket()
	currentRoom = None
	joinedRooms = []
	roomList = []

	@pyqtSlot()
	def run(self):
		print "server running!"
		self.s = socket.socket()
		host = socket.gethostname()
		port = 9999
		self.room = "general"
		try:
			self.s.connect((host, port))
		except:
			self.errorSignal.emit()
			return
		print 'Connected to', host
		self.z = None
		#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
		#if more than the set time passes
		self.s.settimeout(0.01)
		#Continuously look for user and server messages
		while True:
			try:
				received = self.s.recv(1024)
				if received.split()[0] == "/listroom":
					x = received.split()
					x = x[1:]

					self.roomListSignal.emit(" ".join(str(i) for i in x))
				else:
					self.messageSignal.emit(received)
			except (socket.timeout):
				#No input received
				pass
			if self.z is not None:
				self.s.send(self.z)
				print self.z
				self.z = None

	def send_message(self,msg):
		self.z = "/addmessage {} {}".format(self.room,msg)

	def create_room(self,msg):
		self.z = "/createchatroom {}".format(msg)

	def leave_room(self,msg):
		self.z = "/leavechatroom {}".format(msg)
		self.room = None

	def join_room(self,msg):
		self.z = "/joinchatroom {}".format(msg)
		self.room = msg





# ---EVERYTHING BELOW HERE IS OLD AND NOT USED---








def check_for_input(self):
	print "checking input!"
	global z
	try:
		while True:
			z = raw_input("")
			#z = gui.gui_input()
			print z
	except KeyboardInterrupt:
		s.shutdown(socket.SHUT_RDWR)
		s.close()


def server_stuff():
	print "server running!"
	s = socket.socket()
	host = socket.gethostname()
	port = 9999

	try:
		s.connect((host, port))
	except:
		#gui.no_connection()
		print "could not connect A"
	print 'Connected to', host
	z = None

	#This causes all socket operations on s to timeout (Throw a socket.timemout exception)
	#if more than the set time passes
	s.settimeout(0.01)



	#Continuously look for user and server messages
	while True:
		'''try:
			#print '\n'+'\t'+'\t'+s.recv(1024)
			#gui.gui_output(None,s.recv(1024))
		except (socket.timeout):
			#No input received
			pass'''
		if z is not None:
			for i in z:
				s.send(z)
			z = None

if __name__ == "__main__":
	#Start the input method as a second thread
	print "START THE APP FROM THE GUI FOOL"
