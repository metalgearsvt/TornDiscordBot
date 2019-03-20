import sqlite3

conn = sqlite3.connect('torn.db')

c = conn.cursor()
c.execute('''CREATE TABLE users
				(discordId text PRIMARY KEY, apiKey text)''')

conn.commit()
conn.close()