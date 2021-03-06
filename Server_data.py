from Server_chatroom import server_chatroom
from User import user

class server_data:
	chatrooms = None
	users = None

	def __init__(self):
		self.chatrooms = []
		self.users = []

	# Create a new chatroom. Return false if the chatroom cannot be found
	def add_chatroom(self, name):
		for r in self.chatrooms:
			if r.get_name() == name:
				return False
		room = server_chatroom(name)
		self.chatrooms.append(room)
		return True
	
	# Delete a chatroom. Return false if the chatroom cannot be found
	# Also remove any users currently in the chatroom
	def remove_chatroom(self, name):
		for r in self.chatrooms:
			if r.get_name() == name:
				for u in r.get_user_list():
					u.leave_chatroom(r)
				self.chatrooms.remove(r)
				return True
		return False

	# Returns a list of the names (string list) of all chatrooms
	def list_chatrooms(self):
		returnVal = " "
		for i in self.chatrooms:
			returnVal += "\n" + i.get_name()
		return returnVal
	
	# Returns all messages in a chatroom, formatted as a string
	def chatroom_history(self, name):
		for r in self.chatrooms:
			if r.get_name() == name:
				returnVal = ""
				li = r.get_history()
				for i in li:
					returnVal += i + "\n"
				return returnVal
		return False

	#input: message as a string, room name as a string
	#Returns a list of username/connection tuples,
	#or false if the chat room doesn't exist
	def add_message(self, message, roomName):
		for r in self.chatrooms:
			if r.get_name() == roomName:
				users = r.add_message(message)
				returnVal = []
				for u in users:
					returnVal.append((u.get_connection(),u.get_username()))
				return returnVal
		return False

	#Creates a new user object with the desired name, and returns true.
	#Returns false if the username is already in use.
	#If the user is a returning permanent user, return a list of chat rooms they are in
	def add_user(self, userName, conn):
		for u in self.users:
			if u.get_username() == userName:
				if u.get_connection is not None:
					return False
				else:
					retVal = []
					for r in u.get_chatrooms:
						retVal.append(r.get_name)
					return retVal
		newUser = user(userName, conn)
		self.users.append(newUser)
		return True

	#Removes a user from the list of users and all chatrooms they are part of
	#Returns false if the user is not in the list (or offline for permanent users)
	def remove_user(self, userName):
		for u in self.users:
			if u.get_username() == userName:
				#Check if user is a permanent user
				if u.get_permanent_user():
					#If user is already offline, return False
					if u.get_connection is None:
						return False
					#If permanent user is online, set their connection to None
					#and return True
					else:
						u.set_connection(None)
						return True
				#If user is guest user, remove them from all chat rooms
				#and delete their user object
				else:
					for r in u.get_chatrooms():
						r.remove_user(userName)
					self.users.remove(u)
					return True
		return False

	#Makes a user permanent
	#Returns false if username is not in list
	def register_user(self, userName):
		for u in self.users:
			if u.get_username == userName:
				u.make_permanent()
				return True
		return False

	#Returns a list of all usernames and their connections (in tuple form)
	def list_users(self):
		returnVal = []
		for u in self.users:
			returnVal.append((u.get_username(), u.get_connection()))
		return returnVal

	#Links a user to a chat room, and returns the chat room history
	#Returns false if the user or room cannot be found or if they are already linked
	def link_user_chatroom(self, userName, roomName):
		for r in self.chatrooms:
			if r.get_name() == roomName:
				for u in r.get_user_list():
					if u.get_username() == userName:
						return False
				for u in self.users:
					if u.get_username() == userName:
						r.add_user(u)
						u.add_chatroom(r)
						return True#r.get_history()
				return False
		return False

	#Unlinks a user from a chat room
	#Returns false if the user isn't in the chat room, or if the chat room
	#does not exist
	def unlink_user_chatroom(self, userName, roomName):
		for r in self.chatrooms:
			if r.get_name() == roomName:
				for u in r.get_user_list():
					if u.get_username() == userName:
						r.remove_user(u)
						u.leave_chatroom(r)
						return True
				return False
		return False
