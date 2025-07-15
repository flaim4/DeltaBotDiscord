from disnake.ext import commands
import disnake
import time
from util.db import Data
from util.balance import Balance
from util._init_ import Indelifer, CogBase

@Indelifer("is_voice_time")
class isVoiceTime(CogBase):  
    async def init(self):
        self.heshmap = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        server_id = member.guild.id

        async with Data.users as users:
            row = None
            
            if before.channel is None and after.channel is not None:
                users.execute("""SELECT * FROM Users WHERE server_id = ? AND user_id = ?""", (server_id, member.id,))
                row = users.fetchone()
                
                if row is None:
                    users.execute("""INSERT INTO Users (server_id, user_id, voice_activ) VALUES (?, ?, ?)""",
                                (server_id, member.id, 0))
                    await users.commit()
                    users.execute("""SELECT * FROM Users WHERE server_id = ? AND user_id = ?""", (server_id, member.id,))
                    row = users.fetchone()

                self.heshmap[member.id] = time.time()

            elif before.channel is not None and after.channel is None:
                if member.id in self.heshmap:
                    start_time = self.heshmap.pop(member.id)
                    end_time = time.time()

                    if row is None:
                        users.execute("""SELECT * FROM Users WHERE server_id = ? AND user_id = ?""", (server_id, member.id))
                        row = users.fetchone()

                    if row:
                        voice_time = row[3] + (end_time - start_time)
                        users.execute("""UPDATE Users SET voice_activ=? WHERE server_id=? AND user_id=?""",
                                    (voice_time, server_id, member.id,))
                        await users.commit()

                        hours_spent = int((end_time - start_time) // 3600)
                        if hours_spent > 0:
                            reward = hours_spent * 20
                            await Balance.addBalance(server_id, member.id, reward)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for voice_channel in guild.voice_channels:
                for member in voice_channel.members:
                    if not member.bot:
                        self.heshmap[member.id] = time.time()

    @commands.slash_command(default_member_permissions=disnake.Permissions(administrator=True))
    async def sava_time_voice(self, ctx):
        for guild in self.bot.guilds:
            for voice_channel in guild.voice_channels:
                for member in voice_channel.members:
                    if not member.bot:
                        async with Data.users as users:
                            start_time = self.heshmap.pop(member.id, time.time())
                            end_time = time.time()

                            users.execute(
                                """SELECT voice_activ FROM Users WHERE server_id = ? AND user_id = ?""",
                                (guild.id, member.id),
                            )
                            row = users.fetchone()

                            voice_time = (row[0] if row else 0) + (end_time - start_time)

                            if row:
                                users.execute(
                                    """UPDATE Users SET voice_activ = ? WHERE server_id = ? AND user_id = ?""",
                                    (voice_time, guild.id, member.id),
                                )
                            else:
                                users.execute(
                                    """INSERT INTO Users (server_id, user_id, voice_activ) VALUES (?, ?, ?)""",
                                    (guild.id, member.id, voice_time),
                                )

                            await users.commit()

                            hours_spent = int((end_time - start_time) // 3600)
                            if hours_spent > 0:
                                reward = hours_spent * 20
                                await Balance.addBalance(guild.id, member.id, reward)