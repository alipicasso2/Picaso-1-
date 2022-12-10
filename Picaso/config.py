data = {
    "token": ""
}

ticket_panel = {
    "header":"Ticket",
    "description":"Click on Make Ticket to Create a Ticket",
    "button": {
        "text":"Make a Ticket",
        "emoji":"📝"
    },
    "limit": 1
}


def token() -> str: return data["token"]
def panelHeader(): return ticket_panel['header']
def panelDescription(): return ticket_panel["description"]
def panelButtonText(): return ticket_panel['button']['text']
def panelButtonEmoji(): return ticket_panel["button"]['emoji']
def ticketCreateLimite(): return ticket_panel["limit"]
