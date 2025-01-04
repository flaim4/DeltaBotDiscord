import disnake
from disnake.ext import commands
from disnake import Embed
from disnake.ui import Button, View
from util.PageShop import *
from disnake.interactions.application_command import ApplicationCommandInteraction

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.page = PageShop()
        self.manager = PageShopManager(items_per_page=3)
        self.manager.load_items(self.page.list)

    @commands.slash_command()
    async def shop(self, ctx: ApplicationCommandInteraction):
        await ctx.response.defer()

        get_current_page = self.manager.get_current_page()
        if not get_current_page:
            await ctx.send("Магазин пуст")
            return
        
        START_SHOP = Embed(color=0x2b2d31).set_image(url="https://media.discordapp.net/attachments/1235315817445331008/1324551566841352345/Frame_185.png?ex=67793906&is=6777e786&hm=9a7fef4793e0b22bd5cbdd1bf4ed7994a6f656be54fa2896094149436580fa6f&=&format=webp&quality=lossless&width=687&height=231")
        END_SHOP = Embed(title="Магазин личных ролей", color=0x2b2d31).set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png?ex=6779be01&is=67786c81&hm=fecc9b8d4e9e997a0b49306731f92ac8e67e4e52c9a631a2076135b66e8048e8&").set_thumbnail(url=ctx.author.avatar)

        for item in get_current_page:
            END_SHOP.add_field(
                name=f"ID: {item['id']}",
                value=f"Роль: <@&{item['role']}>\nПродавец: <@{item['user']}>\nЦена: {item['price']}",
                inline=False
            )

        buttons = View()
        buttons.add_item(Button(label="Далее", custom_id="next_page"))
        buttons.add_item(Button(label="Назад", custom_id="prev_page"))

        await ctx.send(embeds=[START_SHOP, END_SHOP], view=buttons)

    @commands.slash_command()
    async def add_role_in_shop(self, ctx: ApplicationCommandInteraction, role: disnake.Role, price: int):
        self.page.addRole(role.id, ctx.author.id, price)
        self.manager.load_items(self.page.list)
        await ctx.send(f"Роль {role.mention} добавлена в магазин по цене {price} монет.")

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        await inter.response.defer()

        if inter.component.custom_id == "next_page":
            self.manager.next_page()
        elif inter.component.custom_id == "prev_page":
            self.manager.previous_page()

        get_current_page = self.manager.get_current_page()
        if not get_current_page:
            await inter.response.send_message("Магазин пуст", ephemeral=True)
            return
        START_SHOP = Embed(color=0x2b2d31).set_image(url="https://media.discordapp.net/attachments/1235315817445331008/1324551566841352345/Frame_185.png?ex=67793906&is=6777e786&hm=9a7fef4793e0b22bd5cbdd1bf4ed7994a6f656be54fa2896094149436580fa6f&=&format=webp&quality=lossless&width=687&height=231")
        END_SHOP = Embed(title="Магазин личных ролей", color=0x2b2d31).set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png?ex=6779be01&is=67786c81&hm=fecc9b8d4e9e997a0b49306731f92ac8e67e4e52c9a631a2076135b66e8048e8&").set_thumbnail(url=inter.author.avatar)

        for item in get_current_page:
            END_SHOP.add_field(
                name=f"ID: {item['id']}",
                value=f"Роль: <@&{item['role']}>\nПродавец: <@{item['user']}>\nЦена: {item['price']}",
                inline=False
            )

        await inter.edit_original_response(embeds=[START_SHOP ,END_SHOP])

def setup(bot):
    bot.add_cog(Shop(bot))
