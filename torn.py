import discord
import asyncio
import time
import re
import sqlite3
from conf.config import Config
from util.ParseMsg import ParseMsg

client = discord.Client()

conn = sqlite3.connect('torn.db')

@client.event
async def on_ready():
	print('Logged in as: ' + client.user.name + ' / ' + client.user.id)
	print('------')

@client.event
async def on_message(message):
	print(str(message.channel) + ' - ' + str(message.author) + ': ' + str(message.content))
	if ParseMsg.messageValid(message):
		response = ParseMsg.getMsgResponse(message, conn)
		await client.send_message(response.channel, response.message)

#	if message.content.startswith('!test'):
#		counter = 0
#		tmp = await client.send_message(message.channel, 'Calculating messages...')
#		async for log in client.logs_from(message.channel, limit=100):
#			if log.author == message.author:
#				counter += 1
#		await client.edit_message(tmp, 'You have {} messages.'.format(counter))
#		print('You have {} messages.'.format(counter))
#	elif message.content.startswith('!status'):
#		genChannel = client.get_channel("284185190245597184")
#		await client.send_message(genChannel, 'Status requested.') 
#	elif message.author != client.user:
#		await client.send_message(message.channel, 'Fuck you.')
		
client.run(Config.TOKEN)