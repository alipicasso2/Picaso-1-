import nextcord
import config
import debug

from handlers.Serial import getSerial
from databases.DBManager import Manager
from nextcord.ext import commands
from commands.ticket._TICKET import Status

DEBUG_MOD = False


async def init(interaction: nextcord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
    except:
        pass

    isLimited = await limited(interaction)
    if DEBUG_MOD: debug.info("[CreateTicket] ==> init")
    if isLimited:
        if DEBUG_MOD: debug.info(f"[CreateTicket] ==> interaction_button( {interaction.user.name} ) Has limited")
        Deny_embed = denyEmbed()
        await interaction.followup.send(embed=Deny_embed, ephemeral=True, delete_after=2)
        return

    Prepair_embed = prepairEmbed()
    resp: nextcord.WebhookMessage = await interaction.followup.send(embed=Prepair_embed, ephemeral=True)

    isCreated = await createTicket(interaction)

    if isCreated is False:
        if DEBUG_MOD: debug.error(f"[CreateTicket] ==> interaction_button( {interaction.user.name} ) Failed to create")
        fail_Embed = failEmbed()
        await resp.edit(embed=fail_Embed, delete_after=2)
        return

    if DEBUG_MOD: debug.info(f"[CreateTicket] ==> interaction_button( {interaction.user.name} ) Created successfully")
    Success_embed = successEmbed(isCreated)
    await resp.edit(embed=Success_embed, delete_after=30)


async def limited(interaction: nextcord.Interaction) -> None:
    database = Manager.Tickets(interaction.guild.id)
    tickets = await database.getAllTickets(interaction.guild.id, 'user_id', interaction.user.id)
    Valid_Tickets = 0
    for index, ticket in enumerate(tickets):
        _Channel_id = ticket[0]
        _Channel = interaction.guild.get_channel(int(_Channel_id))
        print(ticket[2])
        if _Channel is None:
            await database.updateTicket(interaction.guild.id, _Channel_id, Status.DELETE, 0)
        if ticket[2] == Status.OPEN:
            Valid_Tickets += 1

    if Valid_Tickets + 1 > config.ticketCreateLimite():
        return True
    return False


async def createTicket(interaction: nextcord.Interaction) -> None:
    """Start ticket Create"""
    try:
        # Importing Databases
        _DBP = Manager.TicketPanels(interaction.guild.id)
        _DB = Manager.Tickets(interaction.guild.id)

        _Panel = await _DBP.getPanel(guildID=interaction.guild.id, Condition='channel_id',
                                     ConditionAnswer=interaction.channel.id)
        _DBP.db.close()

        _Category_IDs = (_Panel[2], _Panel[3])
        _Category: nextcord.CategoryChannel = interaction.guild.get_channel(int(_Panel[2]))

        _Tickets = await _DB.getAllTickets(interaction.guild.id)
        _Tickets_Size = len(_Tickets) + 1

        _Ticket_Channel = await createTicketChannel(interaction, _Category, _Tickets_Size)

        if DEBUG_MOD: debug.info(f"[CreateTicket] ==> {_Ticket_Channel} has Created !")

        # Adding Ticket into database
        await _DB.addTicket(
            guildID=interaction.guild.id,
            channelID=_Ticket_Channel.id,
            userID=interaction.user.id,
            openCategoryID=_Category_IDs[0],
            closeCategoryID=_Category_IDs[1]
        )

        # Closing Ticket DataBase
        _DB.db.close()

        if DEBUG_MOD: debug.info(f"[CreateTicket] ==> {_Ticket_Channel} added into database !")

        # Sending panel into the Ticket
        _Ticket_panel = ticketPanelEmbed(interaction, _Tickets_Size)
        _Ticket_panel_Btn = ticketPanelButton()

        await _Ticket_Channel.send(content=f"||@here||", embed=_Ticket_panel,
                                   view=_Ticket_panel_Btn)

        return _Ticket_Channel
    except Exception as err:
        debug.error(f"Error in CreateTicket.py from CreateTicket :\n{err}")
        return False


async def createTicketChannel(interaction: nextcord.Interaction,
                              _Category: nextcord.CategoryChannel,
                              _Number: int
                              ) -> nextcord.TextChannel:
    _Permissions = {
        interaction.guild.default_role: nextcord.PermissionOverwrite(
            view_channel=False,
            send_messages=False
        ),
        interaction.user: nextcord.PermissionOverwrite(
            view_channel=True,
            send_messages=True
        )
    }

    _Channel = await interaction.guild.create_text_channel(
        name=f"🔓ticket-{'{:0>4}'.format(str(_Number))}",
        category=_Category,
        overwrites=_Permissions
    )

    return _Channel


def prepairEmbed() -> nextcord.Embed:
    embed = nextcord.Embed()
    embed.set_author(name="Preparing ...")
    embed.description = "We are creating your Ticket, Please be Patient !"
    embed.color = nextcord.Color.green()
    return embed


def denyEmbed() -> nextcord.Embed:
    embed = nextcord.Embed()
    embed.set_author(name="Error")
    embed.description = f"Sorry but you can't create Ticket more than {config.ticketCreateLimite()} Ticket"
    embed.color = nextcord.Color.red()
    return embed


def failEmbed() -> nextcord.Embed:
    embed = nextcord.Embed()
    embed.set_author(name="Error")
    embed.description = f"Failed to create your ticket\n`Please tell this problem to Developer or __Try again__`"
    embed.color = nextcord.Color.red()
    return embed


def successEmbed(channel: nextcord.TextChannel) -> nextcord.Embed:
    embed = nextcord.Embed()
    embed.set_author(name="Successful !")
    embed.description = f"Ticket channel is {channel.mention}"
    embed.color = nextcord.Color.green()
    return embed


def ticketPanelEmbed(interaction: nextcord.Interaction, _Number: int) -> nextcord.Embed:
    Serial = getSerial()
    embed = nextcord.Embed()
    embed.set_author(name=f"Ticket {'{:0>4}'.format(str(_Number))}")
    embed.description = f"Hello {interaction.user.mention} \n" \
                        "\✅ Already you are in __Ticket__ and now you can tell your __**Problems**__ to __Supporters__ or __Admins__ \n\n" \
                        "`if you want to close the Ticket , click on 🔒Close Button`"
    embed.color = nextcord.Color.blurple()
    embed.add_field(name="Serial Code",value=f"||{Serial}||")
    return embed


class ticketPanelButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Close", emoji="🔒", style=nextcord.ButtonStyle.blurple, custom_id="close_ticket")
    async def open_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
