import disnake
from disnake.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
from io import BytesIO

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_avatar(self, avatar_url: str) -> Image:
        """Обрабатывает аватар, чтобы сделать его круглым и изменить размер."""
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                avatar: Image = Image.open(BytesIO(await response.read())).convert("RGBA")

        avatar = avatar.resize((156, 156), Image.LANCZOS)

        mask = Image.new("L", (156, 156), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 154, 154), fill=255)

        rounded_avatar = Image.new("RGBA", (156, 156))
        rounded_avatar.paste(avatar, (0, 0), mask)

        return rounded_avatar

    def create_progress_bar(self, current_xp, max_xp, width=676, height=40) -> Image:
        """Создает изображение с прогресс-баром с закругленными углами."""
        bar_image: Image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(bar_image)

        filled_width = int(width * (current_xp / max_xp))

        draw.rounded_rectangle([0, 0, width, height], radius=19, fill=(33, 33, 33, 255))

        draw.rounded_rectangle([0, 0, filled_width, height], radius=19, fill=(39, 188, 143, 255))

        return bar_image

    def renderLevelImage(self, text: str, avatar: Image, current_xp: int, max_xp: int):
        """Рендерит изображение уровня с текстом, аватаром и прогресс-баром."""
        background: Image = Image.open('C:/code/pyDiscord/img/Level.png')

        background.paste(avatar, (23, 23), avatar)

        progress_bar = self.create_progress_bar(current_xp, max_xp)

        background.paste(progress_bar, (200, 139), progress_bar)

        font = ImageFont.truetype('C:/code/pyDiscord/font/Montserrat-SemiBold.ttf', size=41)

        draw: ImageDraw = ImageDraw.Draw(background)
        draw.text((203, 23), text, font=font, fill="white")

        background.save('output_image.png', format='PNG')

    @commands.slash_command(name="level")
    async def Level(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
        if member is None:
            member = ctx.author

        text = f"{member.name}"
        avatar_url = str(member.display_avatar.url)

        current_xp = 56
        max_xp = 1000 

        rounded_avatar = await self.process_avatar(avatar_url)

        self.renderLevelImage(text, rounded_avatar, current_xp, max_xp)

        with open('output_image.png', 'rb') as f:
            await ctx.send(file=disnake.File(f, 'LevelImage.png'))

def setup(bot):
    bot.add_cog(Profile(bot))
