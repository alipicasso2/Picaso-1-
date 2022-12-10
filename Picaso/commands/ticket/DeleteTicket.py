import nextcord
import debug
import asyncio

from commands.ticket._TICKET import Status
from databases.DBManager import Manager

DEBUG_MOD = True


async def init(interaction: nextcord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
    except:
        pass
    _Channel: nextcord.TextChannel = interaction.channel
    await _Channel.send(
        embed=nextcord.Embed(description="Ticket will be deleted in a few seconds", color=nextcord.Color.red()))
    await asyncio.sleep(2)
    _DB = Manager.Tickets(guildID=interaction.guild.id)
    await _DB.updateTicket(interaction.guild.id, _Channel.id, Status.DELETE, 0)
    _DB.db.close()
    await _Channel.delete()
