import disnake 
from disnake.ext import commands
import sqlite3

class мут(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("data.db")
        self.conn1 = sqlite3.connect("mods.db")

    @commands.slash_command(description="Выдать мут")
    @commands.default_member_permissions(move_members=True)
    async def мут(self, ctx, user: disnake.Member, reason:str = None):
        if ctx.author.bot:
            return
        author = ctx.author.name
        author_id = ctx.author.id
        name = ctx.author.display_name
        channel = self.bot.get_channel(1179487135410176133)
        if reason is None:
            reason = 'Причина не указана'
        user_id = user.id
        embed = disnake.Embed(description=f"Модератор <@{author_id}> выдал мут пользователю <@{user.id}>",
                    colour=0x2b2d31)

        embed.set_author(name="Ghost World",
                icon_url="")

        embed.add_field(name="Причина",
                value=f"```{reason}```",
                inline=False)
        await channel.send(embed=embed, components=[
            disnake.ui.Button(
                label="Отменить мут",
                style=disnake.ButtonStyle.danger,
                custom_id="backmute"
            )
        ])
        print(author, "дал мут", user, "по причине:", reason)
        
        embed1 = disnake.Embed(description="Вы выдали мут")
        embed1.set_author(name="Ghost World",
                icon_url="")
        await ctx.send(embed=embed1, ephemeral=True, components=[
            disnake.ui.Button(
                label="Отменить мут",
                style=disnake.ButtonStyle.danger,
                custom_id="ubackmute"
            )
        ])

        server_id = ctx.guild.id


        # Добавить статистику учаснику
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                    (server_id, user.id,))
        row = cur.fetchone()
        if row is None:
            cur.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, balance, time_voice, warning, mes) VALUES (?,?,?,?,?,?,?,?,?)""",
                        (server_id, user.name, user.id, 0, 0, 0, 0, 0, 0))
            self.conn.commit()
            cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                        (server_id, user.id,))
            row = cur.fetchone()
            warn = row[7]
            warn += 1
            cur.execute("""UPDATE users SET warning=? WHERE server_id=? AND user_id=?""", (warn, ctx.guild.id, user.id,))
            self.conn.commit()
        else:
            warn = row[7]
            warn += 1
            cur.execute("""UPDATE users SET warning=? WHERE server_id=? AND user_id=?""", (warn, ctx.guild.id, user.id,))
            self.conn.commit()


        # Добавить статистику модератору
        cur1 = self.conn1.cursor()
        cur1.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                    (server_id, author_id,))
        row1 = cur1.fetchone()
        if row1 is None:
            cur1.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, rate) VALUES (?,?,?,?,?,?)""",
                        (server_id, author, author_id, 0, 0, 0))
            self.conn1.commit()
            cur1.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                        (server_id, author_id,))
            row1 = cur1.fetchone()
            rate = row1[5]
            xp = row1[4]
            rate += 0.3
            xp += 5
            cur1.execute("""UPDATE users SET rate=? WHERE server_id=? AND user_id=?""", (rate, ctx.guild.id, author_id,))
            cur1.execute("""UPDATE users SET xp=? WHERE server_id=? AND user_id=?""", (xp, ctx.guild.id, author_id,))
            self.conn1.commit()
        else:
            rate = row1[5]
            xp = row1[4]
            rate += 0.3
            xp += 5
            cur1.execute("""UPDATE users SET rate=? WHERE server_id=? AND user_id=?""", (rate, ctx.guild.id, author_id,))
            cur1.execute("""UPDATE users SET xp=? WHERE server_id=? AND user_id=?""", (xp, ctx.guild.id, author_id,))
            self.conn1.commit()


    @мут.error
    async def мут_error(self, ctx, error):
        author = ctx.author
        name = ctx.author.display_name
        embed = disnake.Embed(description="У вас не достаточно прав для использования данной команды",
                       colour=0x2b2d31)
        embed.set_author(name=f"{name} • Ошибка 267", icon_url=author.avatar)
        await ctx.send(embed=embed, ephemeral=True)

    def cog_unload(self):
        self.conn.close()
        self.conn1.close()

def setup(bot):
    bot.add_cog(мут(bot))
