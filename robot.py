from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from gpiozero import Buzzer
from time import sleep

# set GPIO
buzzer = Buzzer(17)

# load the secret token from .env file
load_dotenv()
token = os.getenv("TOKEN")
guild = os.getenv("GUILD_ID")

MY_GUILD = discord.Object(id=guild)  # replace with your guild id

# create client class for making slash commands
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

# set intents and create client
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    guilds = [[g.name, g.id] for g in client.guilds]
    print("guilds:", *guilds)

async def beep():
    for _ in range(4):
        for _ in range(4):
            buzzer.on()
            print("on")
            sleep(0.07)
            buzzer.off()
            print("off")
            sleep(0.07)
        sleep(0.4)

# TODO: make it only work in the doors channel
@client.tree.command()
async def doorbell(interaction: discord.Interaction):
    await interaction.response.defer()
    await beep()
    await interaction.followup.send("Ding dong!")

client.run(token)
