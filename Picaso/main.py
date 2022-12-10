import nextcord
import config
import asyncio
import os
import debug

from commands.commands import registerCommands
from handlers import component
from nextcord.ext import commands

intent = nextcord.Intents.all()
bot = commands.Bot(intents=intent)
registerCommands(bot=bot)


@bot.event
async def on_ready():
    debug.info(f'Ticket Bot : All Futures Loaded ! ')


@bot.event
async def on_interaction(interaction: nextcord.Interaction):
    if interaction.type == nextcord.InteractionType.application_command:
        await asyncio.create_task(bot.process_application_commands(interaction))
    elif interaction.type == nextcord.InteractionType.component:
        await asyncio.create_task(component.fetch(interaction))


bot.run(config.token())
