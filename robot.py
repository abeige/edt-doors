# Author: Adam Beigel
# Date: 2023-01-26

import os
import asyncio

from dotenv import load_dotenv
import discord
from discord import app_commands
from gpiozero import LED, TonalBuzzer
from gpiozero.tones import Tone


# define client class
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, guild):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild = guild

    # copies the global commands to the guild
    async def setup_hook(self):
        # run() -> login() -> setup_hook()
        self.tree.copy_global_to(guild=self.guild)
        await self.tree.sync(guild=self.guild)


# load token and guild id from .env file
load_dotenv()
token = os.getenv("TOKEN")
guild = os.getenv("GUILD_ID")
GUILD = discord.Object(id=guild)


# Pi3 GPIO pin for the buzzer
buzzer = TonalBuzzer(pin=17, mid_tone="C6", octaves=1)
notes = ['D5', 'E5', 'G5', 'G5', 'B5', 'A5', 'G5', 'A5', 'A5', 'G5', 'G5', 'A5', 'B5', 'B5', 'D6', 'C6', 'B5', 'C6', 'C6', 'D6', 'B5', 'B5', 'C6', 'D6', 'E6', 'D6', 'C6', 'A5', 'B5', 'C6', 'D6', 'C6', 'B5', 'G5', 'F#5', 'G5', 'B5', 'A5', 'F#5', 'G5']
duration = [0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 1, 1, 1, 2]

async def song(b: TonalBuzzer):
    for n, d in zip(notes, duration):
        d = d/3
        tone = Tone(n)
        buzzer.play(tone.up(4)) # D6 24 up
        await asyncio.sleep(d)
        buzzer.stop()
        await asyncio.sleep(d * 0.1)


# Pi3 GPIO for the LEDs
order = ["red", "green", "blue", "yellow"]
led = {
    "red": LED(6),
    "green": LED(13),
    "blue": LED(19),
    "yellow": LED(26),
}


# flash the lights
async def lights(led):
    while True:
        # go foward
        for i in range(4):
            led[order[i]].on()
            await asyncio.sleep(0.1)
            led[order[i]].off()

        # go back
        for i in range(3, -1, -1):
            led[order[i]].on()
            await asyncio.sleep(0.1)
            led[order[i]].off()


# set intents and create client
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents, guild=GUILD)


# show status on successful login
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    guilds = [[g.name, g.id] for g in client.guilds]
    print("guilds:", *guilds)


# /doorbell command
@client.tree.command()
async def doorbell(interaction: discord.Interaction):
    # TODO: restrict to times when the doors are locked
    if (interaction.channel.name == "doors"):
        await interaction.response.defer()
        
        loop = asyncio.get_event_loop()
        ledTask = asyncio.create_task(lights(led))
        loop.run_until_complete(song(buzzer))
        ledTask.cancel()
        loop.close()

        await interaction.followup.send("Ding dong!")
    else:
        await interaction.response.send_message("This command cannot be used in this channel.")

client.run(token)
