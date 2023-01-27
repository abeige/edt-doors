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
buzzer = TonalBuzzer(pin=17, mid_tone="C7", octaves=1)

notes=[262,294,330,262,262,294,330,262,330,349,392,330,349,392,392,440,392,349,330,262,392,440,392,349,330,262,262,196,262,262,196,262]
duration=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.5,0.5,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,1,0.5,0.5,1]

async def song(b: TonalBuzzer):
    for n, d in zip(notes, duration):
        d = d/2
        tone = Tone(n)
        buzzer.play(tone.up(35))
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
    i = 0
    direction = 1
    for _ in range(85):
        led[order[i]].on()
        await asyncio.sleep(0.1)
        led[order[i]].off()

        # go back and forth
        i += direction
        if i == len(order):
            i -= 2
            direction *= -1
        elif i == -1:
            i += 2
            direction *= -1

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
    # TODO: should only work in the doors channel 
    # TODO: restrict to times when the doors are locked
    await interaction.response.defer()
    await(asyncio.gather(
        song(buzzer),
        lights(led)
    ))
    await interaction.followup.send("Ding dong!")

client.run(token)

