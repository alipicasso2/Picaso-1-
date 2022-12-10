import nextcord
import debug

from commands.ticket._TICKET import Status
from databases.DBManager import Manager

DEBUG_MOD = True


async def init(interaction: nextcord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
    except:
        pass

    # Close Button Pressed
    Open = await TicketIsOpen(interaction)

    if not Open:
        # Sending Fail Embed
        _Embed = notOpenEmbed()
        await interaction.followup.send(embed=_Embed, ephemeral=True, delete_after=1)
        return

    _Channel: nextcord.TextChannel = interaction.channel
    _P = await closeTicketChannel(interaction, _Channel)

    if not _P:
        debug.error("Error in closeTicketChannel in CloseTicket.py : Please contact to Developer")
        return

    _StaffPanelButton = staffPanelButton()
    _StaffPanelEmbed = staffPanelEmbed()
    _StaffPanelMessage = await _Channel.send(embed=_StaffPanelEmbed, view=_StaffPanelButton)

    _DB = Manager.Tickets(interaction.guild.id)
    await _DB.updateTicket(guildID=interaction.guild.id, channelID=_Channel.id, _status=Status.CLOSE,
                           _staffpanelID=_StaffPanelMessage.id)
    _DB.db.close()


async def closeTicketChannel(_Interaction: nextcord.Interaction, channel: nextcord.TextChannel):
    try:
        _Permissions = {
            _Interaction.guild.default_role: nextcord.PermissionOverwrite(
                view_channel=False,
                send_messages=False
            ),
            _Interaction.user: nextcord.PermissionOverwrite(
                view_channel=False,
                send_messages=False
            )
        }

        _DB = Manager.Tickets(_Interaction.guild.id)
        _Ticket = await _DB.getTicket(guildID=_Interaction.guild.id, Condition='channel_id',
                                      ConditionAnswer=_Interaction.channel.id)
        _DB.db.close()
        _Category: nextcord.CategoryChannel = _Interaction.guild.get_channel(int(_Ticket[4]))
        if DEBUG_MOD: debug.info(f"Setting Channel Category to {_Category}")

        await channel.edit(name=f"🔒{channel.name[1:]}", category=_Category, overwrites=_Permissions)

        await channel.send(embed=nextcord.Embed(description=f"Ticket closed by {_Interaction.user.mention}",
                                                color=nextcord.Color.yellow()))

        return True
    except Exception as err:
        if DEBUG_MOD: debug.error("CallBack: "+err)
        return False


async def TicketIsOpen(interaction: nextcord.Interaction):
    _Status = await TicketStatus(interaction)
    if _Status == Status.OPEN:
        return True
    return False


async def TicketStatus(interaction: nextcord.Interaction):
    _DB = Manager.Tickets(interaction.guild.id)
    _Ticket = await _DB.getTicket(guildID=interaction.guild.id, Condition='channel_id',
                                  ConditionAnswer=interaction.channel.id)
    _DB.db.close()
    return _Ticket[2]


def notOpenEmbed() -> nextcord.Embed:
    embed = nextcord.Embed()
    embed.set_author(name="Error")
    embed.description = "Sorry but ticket isn't open"
    embed.color = nextcord.Color.red()
    return embed


def staffPanelEmbed() -> nextcord.Embed:
    embed = nextcord.Embed()
    embed.set_author(name="Staff Panel")
    embed.description = "Hello staffs you can moderate the ticket by above Buttons\n\n" \
                        "\🔓 to Open the Ticket : click on 🔓**Open** Button\n" \
                        "\✂️ to Delete the Ticket : click on ✂️**Delete** Button"
    embed.color = nextcord.Color.blurple()
    return embed


class staffPanelButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Open", emoji="🔓", style=nextcord.ButtonStyle.blurple, custom_id="unlock_ticket",disabled=True)
    async def unlock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction): pass

    @nextcord.ui.button(label="Delete", emoji="✂️", style=nextcord.ButtonStyle.blurple, custom_id="delete_ticket")
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction): pass
