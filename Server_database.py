from Server_chatroom import server_chatroom
from User import user

class server_database:
	chatrooms = None
	users = None
	
	def __init__(self):
		self.chatrooms = []
		self.users = []
	
	def add_chat_room(self, name):
		for r in self.chatrooms:
			if r.get_name() == name:
				return False
		room = server_chatroom(name)
		self.chatrooms.append(room)
		return True
		
	def remove_chat_room(self, name):
		for r in self.chatrooms:
			if r.get_name() == name:
				for u in r.get_user_list():
					u.leave_chatroom(r)
				self.chatrooms.remove(r)
				return True
		return False
	
	def list_chat_rooms(self):
		return self.chatrooms[:]
	
	#input: message as a string, room name as a string
	#Returns a list of username/connection tuples,
	#or false if the chat room doesn't exist
	def add_message(self, message, roomName):
		for r in self.chatrooms:
			if r.get_name() == roomName:
				users = r.add_message(message)
				returnVal = []
				for u in users:
					returnVal.append((u.get_username(), u.get_connection()))
		return False
	
	#Creates a new user object with the desired name, and returns true.
	#Returns false if the username is already in use.
	def add_user(self, userName, conn):
		for u in self.users:
			if u.get_username() == userName:
				return False
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
					for c in u.get_chat_rooms():
						c.remove(userName)
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
	def link_user_chat_room(self, userName, roomName):
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
	def unlink_user_chat_room(self, userName, roomName):
		for r in self.chatrooms:
			if r.get_name == roomName:
				for u in r.get_user_list:
					r.remove_user(u)
					u.leave_chatroom(r)
					return True
		return False
	
#Runs a suite of tests
def main():
	data = server_database()
	
	#Check that adding chatrooms is working correctly
	assert data.add_chat_room("general")
	assert data.add_chat_room("random")
	assert not data.add_chat_room("general")
	assert data.add_chat_room("room3")
	temp = data.list_chat_rooms()
	assert len(temp) == 3
	assert temp[0].get_name() == "general"
	assert temp[1].get_name() == "random"
	assert temp[2].get_name() == "room3"
	
	#Remove an empty chatroom
	data.remove_chat_room("room3")
	assert len(data.list_chat_rooms()) == 2
	
	#Add several users, and tests the list_users functionality
	assert data.add_user("Bob", "blankConn")
	assert data.add_user("Ryan", "blankConn")
	assert data.add_user("Jason", "blankConn")
	assert data.add_user("Daniel", "blankConn")
	assert not data.add_user("Ryan", "blankConn")
	assert data.remove_user("Jason")
	assert not data.remove_user("Jason")
	temp = data.list_users()
	assert len(temp) == 3
	assert temp[0][0] == "Bob"
	assert temp[0][1] == "blankConn"
	assert temp[1][0] == "Ryan"
	assert temp[2][0] == "Daniel"
	
	assert data.link_user_chat_room("Bob", "general")
	assert data.link_user_chat_room("Ryan", "general")
	assert data.link_user_chat_room("Daniel", "general")
	assert not data.link_user_chat_room("Bob", "general")
	assert not data.link_user_chat_room("Ryan", "room3")
	assert not data.link_user_chat_room("Jason", "general")
	
	
main()