import disnake
from disnake.ext import commands
from disnake.ui import Button, View
from disnake import Embed
from util.db import Data


class VoiceLeaders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursor = Data.getCur()
        self.items_per_page = 10
        self.pages = []
        self.current_page_index = 0

    def load_pages(self, server_id):
        self.cursor.execute(
            """
            SELECT user_id, voice_activ 
            FROM Users 
            WHERE server_id = ? 
            ORDER BY voice_activ DESC
            """, 
            (server_id,)
        )
        rows = self.cursor.fetchall()
        self.pages = [
            rows[i:i + self.items_per_page]
            for i in range(0, len(rows), self.items_per_page)
        ]

    def get_current_page(self):
        if self.pages:
            return self.pages[self.current_page_index]
        return []

    @commands.slash_command()
    async def leaders(self, ctx: disnake.ApplicationCommandInteraction, limit: int = 10):
        server_id = ctx.guild.id
        self.items_per_page = limit
        self.load_pages(server_id)

        if not self.pages:
            await ctx.send("Лидеров пока нет!")
            return

        self.current_page_index = 0
        await self.send_leaderboard(ctx)

    async def send_leaderboard(self, ctx):
        current_page = self.get_current_page()
        embed = Embed(title="Лидеры по времени в голосовых каналах", color=0x2b2d31)

        description = ""
        global_index = self.current_page_index * self.items_per_page + 1
        for index, row in enumerate(current_page, start=global_index):
            user_id, voice_time = row

            if voice_time is None:
                voice_time = 0

            days, hours, minutes, _ = self.convert_seconds(voice_time)
            days, hours, minutes = int(days), int(hours), int(minutes)

            medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f"**{index}.**"
            description += f"{medal} <@{user_id}> — {days}д {hours}ч {minutes}м\n"

        if not description:
            description = "Нет данных для отображения."

        embed.description = description
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.set_footer(
            text=f"Страница {self.current_page_index + 1} из {len(self.pages)}"
        )

        buttons = View()
        buttons.add_item(Button(emoji="<:Vector10111:1325288783817605141>", label="Назад", custom_id="prev_page_leader", disabled=self.current_page_index == 0))
        buttons.add_item(Button(emoji="<:Vector1011:1325288770379190283>", label="Далее", custom_id="next_page_leader", disabled=self.current_page_index >= len(self.pages) - 1))

        await ctx.send(embed=embed, view=buttons)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "next_page_leader":
            if self.current_page_index < len(self.pages) - 1:
                self.current_page_index += 1
                await self.update_leaderboard(inter)

        elif inter.component.custom_id == "prev_page_leader":
            if self.current_page_index > 0:
                self.current_page_index -= 1
                await self.update_leaderboard(inter)

    async def update_leaderboard(self, inter):
        current_page = self.get_current_page()
        embed = Embed(title="Лидеры по времени в голосовых каналах", color=0x2b2d31)

        description = ""
        global_index = self.current_page_index * self.items_per_page + 1
        for index, row in enumerate(current_page, start=global_index):
            user_id, voice_time = row

            if voice_time is None:
                voice_time = 0

            days, hours, minutes, _ = self.convert_seconds(voice_time)
            days, hours, minutes = int(days), int(hours), int(minutes)

            medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f"**{index}.**"
            description += f"{medal} <@{user_id}> — {days}д {hours}ч {minutes}м\n"

        if not description:
            description = "Нет данных для отображения."

        embed.description = description
        embed.set_thumbnail(url=inter.author.avatar.url if inter.author.avatar else inter.author.default_avatar.url)
        embed.set_footer(
            text=f"Страница {self.current_page_index + 1} из {len(self.pages)}"
        )

        buttons = View()
        buttons.add_item(Button(emoji="<:Vector10111:1325288783817605141>", label="Назад", custom_id="prev_page_leader", disabled=self.current_page_index == 0))
        buttons.add_item(Button(emoji="<:Vector1011:1325288770379190283>", label="Далее", custom_id="next_page_leader", disabled=self.current_page_index >= len(self.pages) - 1))

        await inter.response.edit_message(embed=embed, view=buttons)

    def convert_seconds(self, seconds):
        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return days, hours, minutes, seconds


def setup(bot):
    bot.add_cog(VoiceLeaders(bot))
