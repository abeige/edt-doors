from dotenv import load_dotenv
import os
import discord
from discord import app_commands

# load the secret token from .env file
load_dotenv()
token = os.getenv("TOKEN")

MY_GUILD = discord.Object(id=1067657862232428564)  # replace with your guild id

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

@client.tree.command()
async def doorbell(interaction: discord.Interaction):
    # TODO: ring the buzzer
    await interaction.response.send_message("Ding dong!")

client.run(token)
