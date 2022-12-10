import nextcord
import asyncio

import commands.ticket.CreateTicket
import commands.ticket.CloseTicket
import commands.ticket.OpenTicket
import commands.ticket.DeleteTicket


async def fetch(interaction: nextcord.Interaction):
    code = interaction.data['custom_id']
    if code == "ticket_button": await asyncio.create_task(commands.ticket.CreateTicket.init(interaction))
    if code == "close_ticket": await asyncio.create_task(commands.ticket.CloseTicket.init(interaction))
    if code == "unlock_ticket": await asyncio.create_task(commands.ticket.OpenTicket.init(interaction))
    if code == "delete_ticket": await asyncio.create_task(commands.ticket.DeleteTicket.init(interaction))
    return