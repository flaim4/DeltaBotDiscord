import disnake 
from disnake.ext import commands
from disnake import TextInputStyle
import sqlite3
import time

class Modal(disnake.ui.Modal):
    def __init__(self):
        components=[
            disnake.ui.TextInput(
                label="Название роли",
                placeholder="А я Артёмка",
                custom_id="rolename",
                style=TextInputStyle.short,
                max_length=100,
            ),
            disnake.ui.TextInput(
                label="Цвет роли",
                placeholder="Пример #ffffff",
                custom_id="rolecolor",
                style=TextInputStyle.short,
                max_length=7,
            ),
        ]
        super().__init__(title="Покупка роли", components=components)
        
    async def callback(self, inter: disnake.ModalInteraction):
            if inter.text_values["rolename"]:
                pass
            elif inter.text_values["rolecolor"]:
                pass

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("data.db")
        self.last_bonus_time = {}


    @commands.slash_command(description="Отображает профиль пользователя.")
    async def профиль(self, ctx, author1: disnake.Member = None):
        if ctx.author.bot:
            return

        if author1 is None:
            author1 = ctx.author

        if author1.bot:
            await ctx.send("Это бот.", ephemeral=True)
            return

        author = ctx.author

        id_server = ctx.guild.id
        id_user = author.id
        name = author.display_name

        cur = self.conn.cursor()


        if author1 is None:
            cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                    (id_server, id_user,))
            result = cur.fetchone()
            if result is None:
                cur.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, balance, time_voice, warning, mes, ocebe, clan, profcolor, lunanrole) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                            (id_server, name, id_user, 0, 0, 0, 0, 0, 0, None, None, None, 0))
                self.conn.commit()

                cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                            (id_server, id_user,))
                result = cur.fetchone()
        else:
            cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                    (id_server, author1.id,))
            result = cur.fetchone()
            if result is None:
                cur.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, balance, time_voice, warning, mes, ocebe, clan, profcolor, lunanrole) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                            (id_server, author1.name, author1.id, 0, 0, 0, 0, 0, 0, None, None, None, 0))
                self.conn.commit()

                cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                            (id_server, author1.id,))
                result = cur.fetchone()
        balance = result[5]
        level = result[3]
        voice_time = result[6]
        xp = result[4]
        warnings = result[7]
        messages = result[8]
        clan = result[9]
        o_cebe = result[10]

        
        общие_минуты = (voice_time// 60) % 60
        общие_часы = (voice_time // 3600)


        if author1 == None:
            embed = disnake.Embed(
                description=f"> **Основная информация**\n```Имя пользователя: {name}\nО себе: {o_cebe}\nКлан: {clan}```",
                colour=0x2b2d31
            )
            embed.set_author(name=f"{name} • Профиль", icon_url=author.avatar)
        else:
            name = author1.display_name
            embed = disnake.Embed(
                    description=f"> **Основная информация**\n```Имя пользователя: {name}\nО себе: {o_cebe}\nКлан: {clan}```",
                    colour=0x2b2d31
                )
            embed.set_author(name=f"{name} • Профиль", icon_url=author1.avatar)

        level_up_threshold = int(10 * (2 ** level))
        embed.add_field(name="> **Уровень**", value=f"```yaml\n💠 {level}```")
        embed.add_field(name="> **Опыт**", value=f"```yaml\n{xp} из {level_up_threshold}```")
        embed.add_field(name="> **Баланс**", value=f"```yaml\n💎 {balance}```")
        embed.add_field(name="> **Нарушения**", value=f"```yaml\n⚠️ {warnings}```")
        embed.add_field(name="> **Активность**", value=f"```yaml\n🕐 {общие_часы}ч {общие_минуты}м```")
        embed.add_field(name="> **Сообщения**", value=f"```yaml\n💬 {messages}```")

        await ctx.send(embed=embed, components=[
            disnake.ui.Button(
                label="⚙️ Настройки",
                style=disnake.ButtonStyle.secondary,
                custom_id="settings"
            ),
            disnake.ui.Button(
                label="🛒 Магазин",
                style=disnake.ButtonStyle.secondary,
                custom_id="buyrole"
            ),
            disnake.ui.Button(
                label="🎁 Бонус",
                style=disnake.ButtonStyle.success,
                custom_id="bonus"
            )
        ])

    async def check_bonus_cooldown(self, author):
        # Проверка времени ожидания перед следующим бонусом
        current_time = time.time()
        last_time = self.last_bonus_time.get(author.id, 0)
        elapsed_time = current_time - last_time
        remaining_time = max(0, 28800 - elapsed_time)

        return remaining_time

    @commands.cooldown(1, 1, commands.BucketType.member)
    @commands.command(name="bonus")
    async def process_bonus(self, ctx):
        author = ctx.author
        remaining_time = await self.check_bonus_cooldown(author)

        min = int(remaining_time // 60) % 60
        h = int(remaining_time // 3600)

        if remaining_time > 0:
            embed = disnake.Embed(description=f"Вы должны подождать еще **{h}** часов **{min}** мин, прежде чем забирать бонус еще раз",
                                  colour=0x2b2d31)
            embed.set_author(name=f"{author.display_name} • Ошибка 105", icon_url=author.avatar)
            await ctx.send(embed=embed, ephemeral=True)
            return

        id_server = ctx.guild.id
        id_user = author.id

        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''', (id_server, id_user,))
        result = cur.fetchone()

        if result:
            balance = result[5]
            balance += 500
            cur.execute("""UPDATE users SET balance = ? WHERE server_id = ? AND user_id = ?""", (balance, id_server, id_user))
            self.conn.commit()

            embed = disnake.Embed(description="На ваш баланс было зачислено `500`💎 Приходите через 8 часов, чтобы забрать следующую награду",
                                  colour=0x2b2d31)

            embed.set_author(name=f"{author.display_name} • Бонус", icon_url=author.avatar)
            await ctx.send(embed=embed, ephemeral=True)

            # Обновляем время последнего использования бонуса для данного пользователя
            self.last_bonus_time[author.id] = time.time()

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.ApplicationCommandInteraction, inter1: disnake.MessageInteraction):
        if inter.component.custom_id == "settings":
            author = inter.author
            name = author.display_name
            embed = disnake.Embed(description="Тут вы можете изменить информацию о себе а так же дать всем понять из какой вы банды",
                                  colour=0x2b2d31)
            embed.set_author(name=f"{name} • Настройки", icon_url=author.avatar)
            await inter.send(embed=embed, ephemeral=True, components=[
                disnake.ui.Button(
                    label="О себе",
                    style=disnake.ButtonStyle.primary,
                    custom_id="setosebe"
                ),
                disnake.ui.Button(
                    label="Клан",
                    style=disnake.ButtonStyle.primary,
                    custom_id="setclan"
                )
            ])

        elif inter.component.custom_id == "setosebe":
            author = inter.author
            name = author.display_name
            embed = disnake.Embed(description="В разработке",
                                  colour=0x2b2d31)
            embed.set_author(name=f"{name} • Ошибка 404", icon_url=author.avatar)
            await inter.send(embed=embed, ephemeral=True)
        
        elif inter.component.custom_id == "setclan":
            author = inter.author
            name = author.display_name
            embed = disnake.Embed(description="В разработке",
                                  colour=0x2b2d31)
            embed.set_author(name=f"{name} • Ошибка 404", icon_url=author.avatar)
            await inter.send(embed=embed, ephemeral=True)

        #elif inter.component.custom_id == "buyrole":
        #    author = inter.author
        #    name = author.display_name
        #
        #    BuyRoleTime = ["Купить роль на 30дней - 30000💎", "Купить роль на 7дней - 7500💎", "Купить роль на 1день - 2500💎"]
        #
        #    embed = disnake.Embed(title="Покупка личной роли",
        #              description="Покупка совершается за серверную валюту 💎\nна определенный срок времени",
        #              colour=0x2b2d31)
        #
        #    embed.set_author(name=f"{author.display_name} • Магазин", icon_url=author.avatar)

            await inter.send(embed=embed, ephemeral=True, components=[
                disnake.ui.StringSelect(
                    custom_id="buycustomrole"
                )
            ])

        elif inter.component.custom_id == "bonus":
            await self.process_bonus(inter)

        elif inter.component.custom_id == "buyrole":
                await inter1.response.send_modal(modal=Modal())



    # @commands.Cog.listener()
    # async def SelectMenu(inter: disnake.MessageInteraction):
    #      if inter.component.custom_id == "buycustomrole":
    #          BuyRoleTime = ["Купить роль на 30дней - 30000💎", "Купить роль на 7дней - 7000💎", "Купить роль на 1день - 2500💎"]
    #          if inter.values[0] == BuyRoleTime[0]:
    #              await inter.response.send_modal(modal=Modal())
    #     await inter.send("ХУЙ")

    def cog_unload(self):
        self.conn.close()


def setup(bot):
    bot.add_cog(Profile(bot))
