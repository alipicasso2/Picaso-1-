import nextcord
import commands.setup as _setup

from nextcord.ext import commands


def registerCommands(bot: nextcord.Client):
    @bot.slash_command(
        description='Initializes the Ticket Bot & Sends a Message to a Channel for Customers to Create Tickets',
        default_member_permissions=nextcord.Permissions(administrator=True))
    async def setup(interaction: nextcord.Interaction, channel: nextcord.TextChannel,
                    open_category: nextcord.CategoryChannel, closed_category: nextcord.CategoryChannel):
        await _setup.execute(interaction=interaction, channel=channel, open_category=open_category,
                             closed_category=closed_category)