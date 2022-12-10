import sqlite3


class Manager:
    class TicketPanels:
        def __init__(self, guildID: int) -> None:
            self.db = sqlite3.connect('./databases/TicketPanel.db')
            self.db.execute(
                f'CREATE TABLE IF NOT EXISTS g_{guildID} (message_id TEXT,channel_id TEXT,open_category_id TEXT,closed_category_id TEXT)')
            self.db.commit()

        async def getPanel(self, guildID: int, Condition: str, ConditionAnswer) -> tuple:
            cur = self.db.cursor()
            cur.execute(
                f"SELECT * FROM g_{guildID} WHERE {Condition}=\'{ConditionAnswer}\'")
            ans = cur.fetchone()
            return ans

        async def getAllPanels(self, guildID: int, Condition: str = None, ConditionAnswer = None) -> tuple:
            cur = self.db.cursor()
            command = f"SELECT * FROM g_{guildID} WHERE {Condition}=\'{ConditionAnswer}\'" if Condition is not None and ConditionAnswer is not None else f"SELECT * FROM g_{guildID}"
            cur.execute(command)
            ans = cur.fetchall()
            return ans

        async def createPanel(self, guildID: int, channelID, messageID: int, openCategoryID: int, closeCategoryID: int):
            cur = self.db.cursor()
            cur.execute(
                f'INSERT INTO g_{guildID}(message_id,channel_id,open_category_id,closed_category_id) VALUES(\'{messageID}\',\'{channelID}\',\'{openCategoryID}\',\'{closeCategoryID}\')')
            self.db.commit()
            cur.close()

        def removePanel(self, guildID: int, Condition: str, ConditionAnswer):
            cur = self.db.cursor()
            cur.execute(
                f"DELETE from g_{guildID} WHERE {Condition}={ConditionAnswer}")
            cur.close()
            return

    class Tickets:
        def __init__(self, guildID: int) -> None:
            self.db = sqlite3.connect('./databases/Ticket.db')
            self.db.execute(
                f"CREATE TABLE IF NOT EXISTS g_{guildID} (channel_id TEXT,user_id TEXT,status TEXT,open_category_id TEXT,close_category_id TEXT,staffpanel_id TEXT)")
            self.db.commit()

        async def addTicket(self, guildID: int, channelID: int, userID: int, openCategoryID: int,
                            closeCategoryID: int) -> None:
            self.db.execute(
                f"INSERT INTO g_{guildID} ( channel_id , user_id , status , open_category_id , close_category_id , staffpanel_id ) VALUES (\'{channelID}\',\'{userID}\',\'OPEN\',\'{openCategoryID}\',\'{closeCategoryID}\',\'0\')")
            self.db.commit()

        async def getAllTickets(self, guildID: int, Condition: str = None, ConditionAnswer = None) -> tuple:
            cur = self.db.cursor()
            if Condition is None and ConditionAnswer is None:
                cmd = f"SELECT * FROM g_{guildID}"
            elif Condition is not None and ConditionAnswer is not None:
                cmd = f"SELECT * FROM g_{guildID} WHERE {Condition} = \'{ConditionAnswer}\'"
            else:
                raise ValueError(f"Condition is {Condition} and ConditionAnswer is {ConditionAnswer} ??")

            cur.execute(cmd)
            resp = cur.fetchall()
            return resp

        async def getTicket(self, guildID: int, Condition: str, ConditionAnswer):
            cur = self.db.cursor()
            cur.execute(
                f"SELECT * FROM g_{guildID} WHERE {Condition} = \'{ConditionAnswer}\'")
            resp = cur.fetchone()
            return resp

        async def updateTicket(self, guildID: int, channelID: int, _status: str, _staffpanelID):
            cur = self.db.cursor()
            cur.execute(f"UPDATE g_{guildID} SET status = \'{_status}\' , staffpanel_id = \'{_staffpanelID}\' WHERE channel_id = \'{channelID}\'")
            self.db.commit()

        async def removeTicket(self, guildID:int, channelID: int):
            cur = self.db.cursor()
            cur.execute(f"DELETE FROM g_{guildID} WHERE channel_id = \'{channelID}\'")
            self.db.commit()