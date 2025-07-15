import disnake
from disnake.ext import commands
from util._init_ import Indelifer, CogBase
from util.db import Data
from disnake.interactions.application_command import ApplicationCommandInteraction
from disnake.ui import View, button as Button
from util.event import subscribe, OnReady
from util.Resouces import loadYamlObject

class TicketButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @Button(label="Закрить тикет", style=disnake.ButtonStyle.green, custom_id="close_ticket_btn")
    async def close_ticket_btn(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        thread = ctx.channel
        if isinstance(thread, disnake.Thread):
            async with Data.tickets as tickets:
                tickets.execute("SELECT id FROM tickets WHERE thread_id = ? AND status = 'open'", (thread.id,))
                ticket = tickets.fetchone()
                if ticket:
                    tickets.execute("UPDATE tickets SET status = 'closed' WHERE thread_id = ?", (thread.id,))
                    await tickets.commit()
                    await ctx.send("Тикет закрыт. Поток будет архивирован.")
                    await thread.edit(archived=True, locked=True)
                else:
                    await ctx.send("Этот тикет уже закрыт или не зарегистрирован.")
        else:
            await ctx.send("Эта кнопка работает только внутри тикет-треда.")

@Indelifer("tikets")
class Tikets(CogBase):

    async def init(self):
        self.support_role_id = 1373322547189514322
        
        self.cfg = loadYamlObject("tiket")
    
    @subscribe(OnReady)
    async def on_ready(self, event : OnReady):
        self.view = TicketButton()
        event.bot.add_view(self.view)
    
    async def create_ticket_internal(self, user: disnake.Member, guild: disnake.Guild, reason: str = "none") -> disnake.Thread:
        async with Data.tickets as tickets:
            channel = guild.get_channel(self.cfg.chanel)
            support_role = guild.get_role(self.cfg.support.role)

            tickets.execute("SELECT thread_id FROM tickets WHERE user_id = ? AND status = 'open'", (user.id,))
            if tickets.fetchone():
                raise Exception("already_open")

            thread = await channel.create_thread(
                name=f"ticket-{user.name}",
                type=disnake.ChannelType.private_thread,
                reason=reason
            )

            await channel.send(content=f"{thread.mention}")
            await thread.add_user(user)

            for member in support_role.members:
                try:
                    await thread.add_user(member)
                except disnake.Forbidden:
                    pass

            tickets.execute("INSERT INTO tickets (user_id, thread_id) VALUES (?, ?)", (user.id, thread.id))
            await tickets.commit()

            ebd = disnake.Embed(description=f"{user.mention}, ваш тикет создан." + 
                    (" Опишите проблему." if reason == "none" else "\nReason:```" + reason + "```"))

            await thread.send(content=f"{support_role.mention}", embed=ebd, view=self.view)

            return thread
    
    @commands.slash_command(name="create_ticket")
    async def create_ticket(self, ctx: disnake.ApplicationCommandInteraction, reason: str = "none"):
        try:
            thread = await self.create_ticket_internal(ctx.user, ctx.guild, reason)
            await ctx.response.send_message(f"Тикет создан: {thread.mention}", ephemeral=True)
        except Exception as e:
            if str(e) == "already_open":
                await ctx.response.send_message("У вас уже есть открытый тикет.", ephemeral=True)
            else:
                raise

    @commands.slash_command(name="close_ticket")
    async def close_ticket(self, ctx: disnake.ApplicationCommandInteraction):
        thread = ctx.channel
        if isinstance(thread, disnake.Thread):
            async with Data.tickets as tickets:
                tickets.execute("SELECT id FROM tickets WHERE thread_id = ? AND status = 'open'", (thread.id,))
                ticket = tickets.fetchone()
                if ticket:
                    tickets.execute("UPDATE tickets SET status = 'closed' WHERE thread_id = ?", (thread.id,))
                    await tickets.commit()
                    await ctx.send("Тикет закрыт. Поток будет архивирован.")
                    await thread.edit(archived=True, locked=True)
                else:
                    await ctx.send("Этот тикет уже закрыт или не зарегистрирован.")
        else:
            await ctx.send("Эта команда работает только внутри тикет-треда.")