import asyncio
from datetime import datetime
import os

import discord

import settings
from utils import (
	is_bot_commander, find_voice_channel_twin, prefix_channel_name,
	unprefix_channel_name, seconds_to_digital
)


print('[+] Initializing bot..')


class CustomClient(discord.Client):

	COUNTDOWN_MESSAGES = (
		':five:',
		':four:',
		':three:',
		':two:',
		':one:',
		f'{settings.CHANNEL_ON_AIR_PREFIX} ON AIR!'
	)

	recording_beginning = None

	@property
	def recording_limit_passed(self):
		"""
		Dicord decided to limit ability to change channel's name.
		In 10 minutes we can change channel's name only 2 times.

		https://stackoverflow.com/questions/62470067/discord-py-bot-renaming-a-voicechannel-only-works-sometimes
		"""
		if self.recording_beginning is None:
			return True

		return self.limit_expires_in == 0
	
	@property
	def limit_expires_in(self):
		"""
		returns in seconds
		"""
		if self.recording_beginning is None:
			return 0

		return max(
			0, settings.CHANNEL_NAME_CHANGE_LIMIT * 60 - (
				datetime.now() - self.recording_beginning
			).total_seconds()
		)

	async def _write_countdown_msg(self, msg, text_channel, voice_client, is_last=False):
		"""
			TODO: Find a way how to load single strema into memory and
				  then reuse it. instead of loading it from file every time.
		"""

		audio_source = discord.FFmpegOpusAudio(
			'media/high_pitch_lq.mp3' if is_last else 'media/low_pitch_lq.mp3'
		)

		await text_channel.send(content=msg)
		if voice_client.is_playing():
			voice_client.stop();

		voice_client.play(audio_source)
		await asyncio.sleep(1)
		audio_source.cleanup()

	async def start_countdown(self, text_channel, voice_channel):
		voice_client = await voice_channel.connect()
		
		await text_channel.send(content='Odpočítavam do začatia vysielania.')
		await asyncio.sleep(1)

		for i, msg in enumerate(self.COUNTDOWN_MESSAGES):
			is_last = i == len(self.COUNTDOWN_MESSAGES) - 1
			await self._write_countdown_msg(msg, text_channel, voice_client, is_last)

		await voice_client.disconnect()


	async def on_ready(self):
		print(f'{self.user} has connected to Discord!')
		
		guild = discord.utils.get(self.guilds, name=settings.DISCORD_GUILD)

		if guild:
			print(
				f'{self.user} is connected to the following guild:\n'
				f'{guild.name}(id: {guild})'
			)
		else:
			print(f'[+] Cannot join to server {settings.DISCORD_GUILD}')

	async def on_message(self, message):
		if not is_bot_commander(message.author) or message.content not in ('!rec_start', '!rec_stop'):
			return

		text_channel = message.channel
		voice_channel_twin = find_voice_channel_twin(message.channel)

		if not voice_channel_twin:
			return

		if message.content == '!rec_start':
			prefixed_name = prefix_channel_name(voice_channel_twin.name)

			if prefixed_name == voice_channel_twin.name:
				await text_channel.send(
					content='Nemôžem spustiť nahrávanie. Voice Kanál je ON AIR...'
				)
				return
			
			if not self.recording_limit_passed:
				readable_expire_time = seconds_to_digital(self.limit_expires_in)
				await text_channel.send(
					content=f'Nemôžem spustiť nahrávanie... Discord Limit expiruje za {readable_expire_time} sekúnd.'
				)
				return

			await self.start_countdown(text_channel, voice_channel_twin)
			self.recording_beginning = datetime.now()
			await voice_channel_twin.edit(name=prefixed_name)

		elif message.content == '!rec_stop':
			unprefixed_name = unprefix_channel_name(voice_channel_twin.name)
			if unprefixed_name == voice_channel_twin.name:
				await text_channel.send(
					content='Nemôžem zastaviť nahrávanie pretože žiadne aktuálne nie je spustené.'
				)
				return

			await voice_channel_twin.edit(name=unprefixed_name)
			await text_channel.send(content='Nahrávanie ukončené!')
			

client = CustomClient()
client.run(settings.DISCORD_TOKEN)
