import discord
import requests
from constant.Constants import Constants as C
class ParseMsg:
	def getJson(endpoint):
		r = requests.get(endpoint)
		return r.json()

	def authorize(message, conn):
		if message.channel.is_private:
			msgList = message.content.split()
			if len(msgList) < 3:
				return Response(C.AUTH_PUB, message.author)
			c = conn.cursor()
			c.execute("INSERT OR REPLACE INTO USERS (discordId, apiKey) values (?, ?)", [message.author.id, msgList[2]])
			conn.commit()
			return Response("Stored API key.", message.author)
		else:
			return Response(C.AUTH_PUB, message.author)

	def battlestats(message, conn):
		c = conn.cursor()
		c.execute("SELECT apiKey FROM USERS WHERE discordId = ?", [message.author.id])
		row = c.fetchone()
		if row == None:
			return Response(C.AUTH_PUB, message.author)
		api_key = row[0]
		endpoint = C.BATTLESTATS_API % api_key
		json = ParseMsg.getJson(endpoint)
		return Response(json, message.channel)


	def messageValid(message):
		msgList = message.content.split()
		if msgList[0] == C.CALL_SIGN:
			return True
		return False

	VALID_CMD = {
		'auth':authorize,
		'battlestats':battlestats
	}
	
	def getMsgResponse(message, conn):
		msgList = message.content.split()
		if len(msgList) < 2:
			return Response(C.HELP, message.channel)
		if len(msgList) >= 2:
			if msgList[1] in ParseMsg.VALID_CMD:
				return ParseMsg.VALID_CMD[msgList[1]](message, conn)
			else:
				return Response(C.INVALID_CMD, message.channel)
				

class Response:
	def __init__(self, message, channel):
		self.message = message
		self.channel = channel