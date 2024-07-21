import discord
import json
import os
import logging
from discord.ext.commands import Bot

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

with open('utils/configData.json') as f:
    configData = json.load(f)

client = Bot(command_prefix = configData['PREFIX'], intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print('Ready to use!')

@client.event
async def on_command_error(interaction: discord.Interaction, error):
    logging.error(f"Erro no comando '{interaction.command}': {error}")
    print(f"Um erro ocorreu: {error}")

async def loadCogs():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'commands.{filename[:-3]}')