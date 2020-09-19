import settings

def is_bot_commander(member):
	for role in member.roles:
		if role.name == settings.BOT_COMMANDER_ROLE:
			return True

	return False


def find_voice_channel_twin(channel):
	"""
	Check if voice channel exists with the same name as specified text channel.
	"""

	unprefixed_name = unprefix_channel_name(channel.name).lower()
	prefixed_name = prefix_channel_name(channel.name).lower()

	for voice_channel in channel.category.voice_channels:
		if voice_channel.name.lower() in (prefixed_name, unprefixed_name):
			return voice_channel


def prefix_channel_name(name):
	if name.startswith(f'{settings.CHANNEL_ON_AIR_PREFIX} '):
		return name

	return f'{settings.CHANNEL_ON_AIR_PREFIX} {name}'


def unprefix_channel_name(name):
	prefix = f'{settings.CHANNEL_ON_AIR_PREFIX} '
	if name.startswith(prefix):
		return name.replace(prefix, '', 1)

	return name


def seconds_to_digital(seconds):
	rounded_seconds = int(seconds)
	minutes = int(rounded_seconds / 60)
	rounded_seconds = int(rounded_seconds - minutes * 60)
	return f'{minutes}:{rounded_seconds}'


