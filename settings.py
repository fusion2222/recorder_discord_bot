import json


CONF = {}
with open('conf.json', 'r') as f:
	CONF = json.loads(f.read())

# Make this configurable
DISCORD_TOKEN = CONF['DISCORD_TOKEN']
DISCORD_GUILD = CONF['DISCORD_GUILD']
BOT_COMMANDER_ROLE = CONF.get('BOT_COMMANDER_ROLE', 'Rekordér')

# Not configurable! Fixed by discord.
CHANNEL_NAME_CHANGE_LIMIT = 10  # minutes. 

CHANNEL_ON_AIR_PREFIX = '\U0001F534'  # Red circle emoji
