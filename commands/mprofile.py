import disnake 
from disnake.ext import commands
import sqlite3

class mProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("mods.db")

    @commands.slash_command(description="Отображает статистику модератора.")
    @commands.default_member_permissions(move_members=True)
    async def статистика(self, ctx, author: disnake.Member = None):
        if author is None:
            author = ctx.author

        if author.bot:
            await ctx.send("Это бот.", ephemeral=True)
            return

        id_server = ctx.guild.id
        id_user = author.id
        name = author.display_name

        cur = self.conn.cursor()

        if author is None:
            cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                    (id_server, id_user,))
            result = cur.fetchone()
            if result is None:
                cur.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, rate) VALUES (?,?,?,?,?,?)""",
                            (id_server, name, id_user, 0, 0, 0))
                self.conn.commit()

                cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                            (id_server, id_user,))
                result = cur.fetchone()
        else:
            cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                    (id_server, author.id,))
            result = cur.fetchone()
            if result is None:
                cur.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, rate) VALUES (?,?,?,?,?,?)""",
                            (id_server, name, id_user, 0, 0, 0))
                self.conn.commit()

                cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                            (id_server, id_user,))
                result = cur.fetchone()
        lvl = result[3]
        xp = result[4]
        rate = result[5]


        ostalos = int(7 * (2 ** lvl))

        if author == None:
            embed = disnake.Embed(colour=0x0f82b3)

            embed.set_author(name=f"{author} • Статистика", icon_url=author.avatar)
            embed.add_field(name="> Опыт:", value=f"```yaml\n{xp} из {ostalos}\n```", inline=True)
            embed.add_field(name="> Уровень", value=f"```yaml\n{lvl}\n```", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1183157891432198184/1186553844486914048/58db3c8d319291af.png?ex=6593ab61&is=65813661&hm=eb4086bae06fc3f8a7de654a9e2d68c644ea4e86e34ed74a4a86369650bfd159&")
        else:
            embed = disnake.Embed(colour=0x0f82b3)

            embed.set_author(name=f"{author} • Статистика", icon_url=author.avatar)
            embed.add_field(name="> Опыт:", value=f"```yaml\n{xp} из {ostalos}\n```", inline=True)
            embed.add_field(name="> Уровень", value=f"```yaml\n{lvl}\n```", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1183157891432198184/1186553844486914048/58db3c8d319291af.png?ex=6593ab61&is=65813661&hm=eb4086bae06fc3f8a7de654a9e2d68c644ea4e86e34ed74a4a86369650bfd159&")


        if rate == 0:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561549225377872/0.png?ex=659af933&is=65888433&hm=f9ec176c42955137f5626758e8971d6495d5b5c2fa159050e9081dde019c6d48&")
        elif rate <= 0.7:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561553226735698/1.png?ex=659af934&is=65888434&hm=fe24bede8bbc97ae39675f8258c51aaad9bddabbee26306edff9cae48731fed9&")
        elif rate <= 1.3:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561567269277696/2.png?ex=659af938&is=65888438&hm=4f6b166d318a028f9ba5412d984c5780a1a3c3b20ef2a6ef8d4299d2aac7b2a7&")
        elif rate <= 1.9:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561586403680346/3.png?ex=659af93c&is=6588843c&hm=2c5553c6b2337dc249a598ff44c982b8332893580d0e1bfea0cb1154ca6acd80&")
        elif rate <= 2.6:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561593815007322/4.png?ex=659af93e&is=6588843e&hm=0418faf3fc4d409bb746f3d57183aa487d9278afafcd1519036b8cacc771fec0&")
        elif rate <= 3.3:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561610369925160/5.png?ex=659af942&is=65888442&hm=af8cfe81b115af19092e85b42af5ca0d854ee287ed3af85a7d4f675373db7b5c&")
        elif rate <= 3.9:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561615772192959/6.png?ex=659af943&is=65888443&hm=5c13deb1f42461c4f57d7b1fd17bf5be994aaf66a9258b63d96ed0f31edd6c52&")
        elif rate <= 4.6:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561622965424178/7.png?ex=659af945&is=65888445&hm=4eb7da697f4b133d79a2cb051246e19f11464cc7a810a6b48464240bb6bfffdc&")
        elif rate <= 5:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561636148129873/8.png?ex=659af948&is=65888448&hm=e8c0bff6821dde227cb51a78acc3c709cfcc93d943ae53a520c55e26cc4d5cee&")
        elif rate <= 5.7:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561644968755230/9.png?ex=659af94a&is=6588844a&hm=f3ea8487c05acce30c9eb4af46354c9a45272d44277eaf67b6c074b6fc9cc255&")
        elif rate <= 6.4:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561653655162952/10.png?ex=659af94c&is=6588844c&hm=343ae4fcb5aba94a88fa64f17bdca71cbdd962b902f61210826117410d32d088&")
        elif rate <= 7.1:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561664455479326/11.png?ex=659af94f&is=6588844f&hm=df73c48a3c6a6a0024d77f8fc9802c2be6087e67e3deb9fcfa1e44149a440699&")
        elif rate <= 7.8:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561672135266464/12.png?ex=659af951&is=65888451&hm=6c261c4efac683c1ad5949388bab3514a86efb514ffa432f5dd48555e06121f2&")
        elif rate <= 8.6:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561681375305839/13.png?ex=659af953&is=65888453&hm=f0ea7de51cf834471a8a5a2fc3ad9478b199f0c4f59627e0b5713930ba70a9c8&")
        elif rate <= 9.1:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561689394806864/14.png?ex=659af955&is=65888455&hm=c582a3e16c4e6dc706ed2821b227cf06ab7b37a990e5e9713f69168286e6dbee&")
        elif rate <= 9.6:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561698131546143/15.png?ex=659af957&is=65888457&hm=05520567ee21adcf960aa2eba16280c96bbd03582ee07091f0fb1ad03b23162b&")
        elif rate >= 10:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name=f"Рейтинг - {rate}")
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1188561481369923715/1188561708487290943/16.png?ex=659af959&is=65888459&hm=d368f4cbd6b746b812c2b83f64a5466717fed84352154946854cf4323e2a6b0c&")
        else:
            embed1 = disnake.Embed(colour=0x0f82b3)

            embed1.set_author(name="ОШИБКА 45")
            embed1.set_image(url="")
        
        
        await ctx.send( embeds=[embed,embed1])


    def cog_unload(self):
        self.conn.close()

def setup(bot):
    bot.add_cog(mProfile(bot))