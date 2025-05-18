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
            cur = Data.getCur()
            cur.execute("SELECT id FROM tickets WHERE thread_id = ? AND status = 'open'", (thread.id,))
            ticket = cur.fetchone()
            if ticket:
                cur.execute("UPDATE tickets SET status = 'closed' WHERE thread_id = ?", (thread.id,))
                Data.commit()
                await ctx.send("Тикет закрыт. Поток будет архивирован.")
                await thread.edit(archived=True, locked=True)
            else:
                await ctx.send("Этот тикет уже закрыт или не зарегистрирован.")
            cur.close()
        else:
            await ctx.send("Эта кнопка работает только внутри тикет-треда.")

@Indelifer("tikets")
class Tikets(CogBase):
    def init(self):
        self.cur = Data.getCur()
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            thread_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        Data.commit()
        
        self.support_role_id = 1373322547189514322
        
        self.cfg = loadYamlObject("tiket")
    
    @subscribe(OnReady)
    async def on_ready(self, event : OnReady):
        self.view = TicketButton()
        event.bot.add_view(self.view)
        
        await event.bot.get_channel(self.cfg.chanel).send(embed=disnake.Embed(description="This channel is for logs, not dialogues. Observe silently."))
    
    async def create_ticket_internal(self, user: disnake.Member, guild: disnake.Guild, reason: str = "none") -> disnake.Thread:
        channel = guild.get_channel(self.cfg.chanel)
        support_role = guild.get_role(self.cfg.support.role)

        self.cur.execute("SELECT thread_id FROM tickets WHERE user_id = ? AND status = 'open'", (user.id,))
        if self.cur.fetchone():
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

        self.cur.execute("INSERT INTO tickets (user_id, thread_id) VALUES (?, ?)", (user.id, thread.id))
        Data.commit()

        ebd = disnake.Embed(description=f"{user.mention}, ваш тикет создан.{' Опишите проблему.' if reason == 'none' else f'\nReason:```{reason}```'}")
        await thread.send(content=f"{support_role.mention}", embed=ebd, view=self.view)

        return thread
    
    @commands.slash_command(name="create_ticket")
    async def c_ticket(self, ctx: disnake.ApplicationCommandInteraction, reason: str = "none"):
        try:
            thread = await self.create_ticket_internal(ctx.user, ctx.guild, reason)
            await ctx.response.send_message(f"Тикет создан: {thread.mention}", ephemeral=True)
        except Exception as e:
            if str(e) == "already_open":
                await ctx.response.send_message("У вас уже есть открытый тикет.", ephemeral=True)
            else:
                raise