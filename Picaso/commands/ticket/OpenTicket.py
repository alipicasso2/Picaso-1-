import nextcord
import debug

from commands.ticket._TICKET import Status
from databases.DBManager import Manager

DEBUG_MOD = True


async def init(interaction: nextcord.Interaction):
    # Open Button Pressed
    try:
        await interaction.response.defer(ephemeral=True)
    except:
        pass

    _Channel: nextcord.TextChannel = interaction.channel
    _P = await openTicketChannel(interaction, _Channel)
    if not _P:
        debug.error("Some error event happened in OpenTicket.py from openTicketChannel")


async def openTicketChannel(interaction, channel: nextcord.TextChannel):
    try:
        debug.info(f"Opening {channel.name} Ticket")
        _DB = Manager.Tickets(interaction.guild.id)
        _Ticket = await _DB.getTicket(guildID=interaction.guild.id, Condition='channel_id',
                                      ConditionAnswer=interaction.channel.id)
        await _DB.updateTicket(guildID=interaction.guild.id, channelID=channel.id, _status=Status.OPEN, _staffpanelID=0)
        _DB.db.close()
        _Category: nextcord.CategoryChannel = interaction.guild.get_channel(int(_Ticket[3]))
        _Author = interaction.guild.get_member(int(_Ticket[1]))

        _Permissions = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(
                view_channel=False,
                send_messages=False
            ),
            _Author: nextcord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )
        }

        # Fetching staffPanel
        _StaffPanelMessage = await channel.fetch_message(_Ticket[5])

        # Removing staffPanel
        await _StaffPanelMessage.delete()

        # Converting Channel into an Open Ticket
        _before_pos = channel.position
        await channel.edit(name=f"🔓{channel.name[1:]}", overwrites=_Permissions, category=_Category)
        await channel.send(embed=nextcord.Embed(description=f"Ticket opened by {interaction.user.mention}",
                                                color=nextcord.Color.green()))
        return True
    except Exception as e:
        debug.error(e)
        return False
