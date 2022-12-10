import nextcord
import sqlite3

def execute(interaction:nextcord.Interaction,role:nextcord.Role):
    print(interaction,role)
    
    
    
class dbr:
    def __init__(self) -> None:
        self.db = sqlite3.connect('./databases/role.db')