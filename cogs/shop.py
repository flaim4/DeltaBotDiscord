import disnake
import re
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
        self.manager = None
        self.server_id = None

    @commands.slash_command()
    async def shop(self, ctx: ApplicationCommandInteraction):
        self.server_id = ctx.guild_id
        self.manager = PageShopManager(items_per_page=6, page_shop=self.page, server_id=self.server_id)

        await ctx.response.defer()

        current_page = self.manager.get_current_page()
        if not current_page:
            embed = Embed(title="Магазин личных ролей", color=0x2b2d31)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        embed = Embed(title="Магазин личных ролей", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.avatar.url)

        for item in current_page:
            embed.add_field(
                name=f"ID: {item['id']}",
                value=f"Роль: <@&{item['role']}>\nЦена: {item['price']} монет",
                inline=False
            )

        embed.set_footer(
            text=f"Страница {self.manager.current_page_index + 1} из {len(self.manager.pages)}"
        )

        buttons = View()

        buttons.add_item(Button(
            emoji="<:Vector10111:1325288783817605141>", label="Назад", custom_id="prev_page", disabled=self.manager.current_page_index == 0
        ))

        buttons.add_item(Button(
            emoji="<:Vector1011:1325288770379190283>", label="Далее", custom_id="next_page", disabled=self.manager.current_page_index >= len(self.manager.pages) - 1
        ))

        buttons.add_item(Button(emoji="<:Frame1193411:1325288755048743024>", label="Купить", custom_id="buy_role", style=disnake.ButtonStyle.success))

        await ctx.send(embed=embed, view=buttons)



    @commands.slash_command(default_member_permissions=disnake.Permissions(administrator=True))
    async def add_role_in_shop(self, ctx: ApplicationCommandInteraction, role: disnake.Role, price: int):
        if self.manager is None:
            self.server_id = ctx.guild.id
            self.manager = PageShopManager(items_per_page=6, page_shop=self.page, server_id=self.server_id)

        bot_highest_role = ctx.guild.me.top_role
        if role >= bot_highest_role:
            await ctx.send(f"Эта роль {role.mention} выше моей должности. Я не могу её добавить в магазин.", ephemeral=True)
            return
        
        existing_role = self.page.get_role_by_role_id(role.id, ctx.guild.id)
        if existing_role:
            await ctx.send(f"Роль <@&{role.id}> уже существует в магазине.", ephemeral=True)
            return

        self.page.add_role(role.id, ctx.author.id, price, ctx.guild.id)
        self.manager.load_pages()
        await ctx.send(f"Роль {role.mention} добавлена в магазин по цене {price} монет.")

    @commands.slash_command(default_member_permissions=disnake.Permissions(administrator=True))
    async def remove_role_in_shop(self, ctx: ApplicationCommandInteraction, id: int):
        removed_role = self.page.remove_role_by_id(id, ctx.guild_id)
        if removed_role:
            self.manager.load_pages()
            await ctx.send(f"Роль <@&{removed_role['role']}> удалена из магазина.")
        else:
            await ctx.send("Роль с указанным ID не найдена.")


    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if self.manager is None:
            return

        if inter.component.custom_id == "confirm_purchase":
            match = re.search(r"<@&(\d+)>", inter.message.embeds[0].description)
            if match:
                role_id = int(match.group(1))
            else:
                await inter.send("Не удалось найти ID роли в описании.", ephemeral=True)
                return

            role = self.page.get_role_by_role_id(role_id, inter.guild_id)

            if role:

                guild_role = inter.guild.get_role(role['role_id'])

                bot_highest_role = inter.guild.me.top_role
                if guild_role >= bot_highest_role:
                    await inter.send(f"Эта роль <@&{guild_role.id}> выше моей должности. Я не могу её выдать.", ephemeral=True)
                    return

                if guild_role in inter.author.roles:
                    await inter.send(f"<@{inter.author.id}>, у вас уже есть эта роль <@&{role['role_id']}>.", ephemeral=True)
                    return
                
                user_balance = Balance.getBalance(inter.guild.id, inter.author.id)
                if int(user_balance) >= int(role['price']):
                    Balance.spendBalance(inter.guild.id, inter.author.id, role['price'])
                    await inter.author.add_roles(inter.guild.get_role(role['role_id']))
                    await inter.send(f"<@{inter.author.id}>, Вы успешно купили роль <@&{role['role_id']}> за {role['price']} монет.")
                    return
                else:
                    await inter.send("У вас недостаточно средств для покупки этой роли.", ephemeral=True)
                    return
            else:
                await inter.send("Роль с таким ID не найдена.", ephemeral=True)
                return

        elif inter.component.custom_id == "cancel_purchase":
            await inter.send("Вы отменили покупку.", ephemeral=True)
            return

        elif inter.component.custom_id == "buy_role":
            await inter.response.send_modal(modal=BuyRoleInShop(self.page))
            return

        elif inter.component.custom_id == "next_page":
            self.manager.next_page()

        elif inter.component.custom_id == "prev_page":
            self.manager.previous_page()

        get_current_page = self.manager.get_current_page()
        if not get_current_page:
            await inter.response.send_message("Магазин пуст", ephemeral=True)
            embed = Embed(title="Магазин личных ролей", color=0x2b2d31)
            embed.set_thumbnail(url=inter.author.avatar)
            await inter.edit_original_response(embeds=[embed], view=None)
            return

        END_SHOP = Embed(title="Магазин личных ролей", color=0x2b2d31)
        END_SHOP.set_thumbnail(url=inter.author.avatar)

        for item in get_current_page:
            END_SHOP.add_field(
                name=f"ID: {item['id']}",
                value=f"Роль: <@&{item['role']}>\nЦена: {item['price']} монет",
                inline=False
            )

        END_SHOP.set_footer(
            text=f"Страница {self.manager.current_page_index + 1} из {len(self.manager.pages)}"
        )

        buttons = View()
        buttons.add_item(Button(emoji="<:Vector10111:1325288783817605141>", label="Назад", custom_id="prev_page", disabled=self.manager.current_page_index == 0))
        buttons.add_item(Button(emoji="<:Vector1011:1325288770379190283>", label="Далее", custom_id="next_page", disabled=self.manager.current_page_index == len(self.manager.pages) - 1))
        buttons.add_item(Button(emoji="<:Frame1193411:1325288755048743024>", label="Купить", custom_id="buy_role", style=disnake.ButtonStyle.success))

        if not inter.response.is_done():
            await inter.response.defer()

        await inter.edit_original_response(embeds=[END_SHOP], view=buttons)

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
        role = self.page_shop.get_role_by_id(role_id, inter.guild_id)

        if not role:
            await inter.send("Роль с таким ID не существует.", ephemeral=True)
            return

        embed = disnake.Embed(
            title="Подтверждение покупки",
            description=f"Вы хотите купить роль <@&{role['role']}> за {role['price']} монет?",
            color=0x2b2d31
        )

        buttons = View()
        buttons.add_item(Button(label="Да", custom_id="confirm_purchase", style=disnake.ButtonStyle.grey))
        buttons.add_item(Button(label="Нет", custom_id="cancel_purchase", style=disnake.ButtonStyle.grey))

        await inter.send(embed=embed, view=buttons, ephemeral=True)


def setup(bot):
    bot.add_cog(Shop(bot))
