import nextcord
import sqlite3
import config

from databases.DBManager import Manager


async def execute(interaction: nextcord.Interaction, channel: nextcord.TextChannel,
                  open_category: nextcord.CategoryChannel, closed_category: nextcord.CategoryChannel) -> None:
    i1 = nextcord.Embed()
    i1.set_author(name="Preparing ...")
    i1.description = "We are working on your Ticket Panel , Please be Patient !"
    i1.color = nextcord.Color.yellow()

    await interaction.response.defer(ephemeral=True)

    db = Manager.TicketPanels(interaction.guild.id)

    can_build = await can_build_new(db, interaction)
    if not can_build:
        a1 = nextcord.Embed()
        a1.set_author(name="</ Error >")
        a1.description = "Please delete the past __Ticket Panel__ to create a new __Ticket Panel__"
        a1.color = nextcord.Color.red()
        await interaction.followup.send(embed=a1, delete_after=2)
        return db.db.close()

    tp = nextcord.Embed()
    tp.set_author(name=config.panelHeader())
    tp.description = config.panelDescription()
    tp.color = nextcord.Color.blue()
    Buttons = buttons()
    msg = await channel.send(embed=tp, view=Buttons)

    await db.createPanel(interaction.guild.id, channel.id, msg.id, open_category.id, closed_category.id)

    successful_Embed = successEmbed(channel, open_category, closed_category)
    await interaction.followup.send(embed=successful_Embed)

    return db.db.close()


def successEmbed(channel, open_category, closed_category) -> nextcord.Embed:
    embed = nextcord.Embed()
    embed.set_author(name="Successful Request !")
    embed.color = nextcord.Color.green()
    embed.description = f"Ticket Panel has created Successfully in **{channel.name}** Channel\n\n" \
                        f"\✅ **Ticket Category :** __{open_category.name}__ `(ID: {open_category.id})`\n" \
                        f"\🛑 **Closed Ticket Category :** __{closed_category.name}__ `(ID: {closed_category.id})`"
    return embed


async def can_build_new(db: Manager.TicketPanels, interaction: nextcord.Interaction):
    foundAnotherPanel = await PanelExists(db, interaction.guild.id)
    if not foundAnotherPanel:
        # database can't find anything's
        return True

    # a result found in database
    return await CheckAllPanels(db, interaction)


async def CheckAllPanels(db: Manager.TicketPanels, interaction: nextcord.Interaction):
    panels = await db.getAllPanels(interaction.guild.id)
    for panel in panels:
        channel = interaction.guild.get_channel(int(panel[1]))
        if channel is not None:
            try:
                await channel.fetch_message(int(panel[0]))
                return False
            except:
                db.removePanel(interaction.guild.id, 'message_id', int(panel[0]))

        else:
            db.removePanel(interaction.guild.id, 'channel_id', int(panel[1]))
    return True


async def PanelExists(db: Manager.TicketPanels, guildID: int):
    panels = await db.getAllPanels(guildID)
    if len(panels) == 0:
        return False
    return True


class buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label=config.panelButtonText(), emoji=config.panelButtonEmoji(),
                        style=nextcord.ButtonStyle.gray, custom_id="ticket_button")
    async def open_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction): pass
