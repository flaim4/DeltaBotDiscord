import disnake
from disnake.ext import commands
from disnake import Embed
from disnake.ui import Button, View
from util.PageShop import *
from util.balance import *
from disnake.interactions.application_command import ApplicationCommandInteraction

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.page = PageShop()
        self.manager = PageShopManager(items_per_page=6)
        self.manager.load_items(self.page.list)

    @commands.slash_command()
    async def shop(self, ctx: ApplicationCommandInteraction):
        await ctx.response.defer()

        get_current_page = self.manager.get_current_page()
        if not get_current_page:
            await ctx.send("Магазин пуст")
            return
        
        END_SHOP = Embed(title="Магазин личных ролей", color=0x2b2d31).set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png?ex=6779be01&is=67786c81&hm=fecc9b8d4e9e997a0b49306731f92ac8e67e4e52c9a631a2076135b66e8048e8&").set_thumbnail(url=ctx.author.avatar)

        for item in get_current_page:
            END_SHOP.add_field(
                name=f"ID: {item['id']}",
                value=f"Роль: <@&{item['role']}>\nЦена: {item['price']}",
                inline=False
            )

        buttons = View()
        buttons.add_item(Button(label="Назад", custom_id="prev_page"))
        buttons.add_item(Button(label="Далее", custom_id="next_page"))
        buttons.add_item(Button(label="Купить", custom_id="buy_role", style=disnake.ButtonStyle.success))

        await ctx.send(embeds=[END_SHOP], view=buttons)

    @commands.slash_command()
    async def add_role_in_shop(self, ctx: ApplicationCommandInteraction, role: disnake.Role, price: int):
        self.page.addRole(role.id, ctx.author.id, price)
        self.manager.load_items(self.page.list)
        await ctx.send(f"Роль {role.mention} добавлена в магазин по цене {price} монет.")

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "buy_role":
            await inter.response.send_modal(modal=BuyRoleInShop(self.page))
            return
        else:
            await inter.response.defer()

        if inter.component.custom_id == "next_page":
            self.manager.next_page()
        elif inter.component.custom_id == "prev_page":
            self.manager.previous_page()

        get_current_page = self.manager.get_current_page()
        if not get_current_page:
            await inter.response.send_message("Магазин пуст", ephemeral=True)
            return

        END_SHOP = Embed(title="Магазин личных ролей", color=0x2b2d31).set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png?ex=6779be01&is=67786c81&hm=fecc9b8d4e9e997a0b49306731f92ac8e67e4e52c9a631a2076135b66e8048e8&").set_thumbnail(url=inter.author.avatar)

        for item in get_current_page:
            END_SHOP.add_field(
                name=f"ID: {item['id']}",
                value=f"Роль: <@&{item['role']}>\nЦена: {item['price']}",
                inline=False
            )

        await inter.edit_original_response(embeds=[END_SHOP])



class BuyRoleInShop(disnake.ui.Modal, Shop):
    def __init__(self, page_shop):
        self.page_shop: PageShop = page_shop
        components = [
            disnake.ui.TextInput(
                label="Введите ID.",
                placeholder="Введите ID роли, которую вы хотите приобрести.",
                custom_id="id_role",
                style=disnake.TextInputStyle.short,
                max_length=3,
            )
        ]
        super().__init__(title="Купить", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        role_id = int(inter.text_values["id_role"])
        role = self.page_shop.get_role_by_id(role_id)
        print(role)
        if not role:
            await inter.send("Роль с таким ID не существует.", ephemeral=True)
            return
        
        user_balance = Balance.getBalance(inter.guild.id, inter.author.id)
        if user_balance >= role["price"]:
            Balance.spendBalance(inter.guild.id, inter.author.id, role["price"])
            await inter.author.add_roles(inter.guild.get_role(role["role"]))
            await inter.send(f"Вы успешно купили роль за {role['price']} монет.")
        else:
            await inter.send("У вас недостаточно средств для покупки этой роли.", ephemeral=True)


def setup(bot):
    bot.add_cog(Shop(bot))
