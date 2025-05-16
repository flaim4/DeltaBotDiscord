import disnake
from disnake.ext import commands
from util.db import Data
import enum
from util.member import Member
from disnake.ext import commands
import settings
from util._init_ import Indelifer

class LeaderType:
    def __init__(self, leaders):
        self.leaders = leaders
        self.type = None
        
    async def execute(self, ctx: disnake.ApplicationCommandInteraction, limit: int, server_id : int, user_id : int, member: disnake.Member, subar : bool):
        pass
    
    def convert_seconds(self, seconds):
        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return days, hours, minutes, seconds

class LeaderVoice(LeaderType):
    def __init__(self, leaders):
        super().__init__(leaders)
        self.type = LeaderTypeEnum.Voice
        
    async def execute(self, ctx: disnake.ApplicationCommandInteraction, limit: int, server_id : int, user_id : int, member: disnake.Member, subar : bool):
        
        self.cursor.execute(
        """
SELECT * FROM Users 
WHERE server_id = ? 
ORDER BY voice_activ DESC 
LIMIT ?;
        """, 
        (server_id, limit))

        rows = self.cursor.fetchall()
        
        text = "### Лидеры по времени в голосовом канале\n"
        
        for index, row in enumerate(rows[:limit], start=1):
            voice_time = row[3]

            if voice_time <= 120:
                continue

            if voice_time is None or voice_time == 0:
                days, hours, minutes, seconds = 0, 0, 0, 0
            else:
                days, hours, minutes, seconds = self.convert_seconds(voice_time)

            medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f"**{index}.**"

            text += f"{medal} <@{row[1]}>\nВремя: {int(days)}д {int(hours)}ч {int(minutes)}м\n\n"

        await ctx.send(
            embed=disnake.Embed(description=text, colour=self.ProfileColor).set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png?ex=66c67201&is=66c52081&hm=269a763945fef2aff03bc746e97d383b8776db4ef7c3771fd3c29b5a853cfdce&"))



        self.cursor.execute(
        "SELECT voice_activ FROM Users WHERE user_id = ? AND server_id = ?;", 
        (user_id, server_id))
        user_voice_activ = self.cursor.fetchone()

        if user_voice_activ:
            user_voice_activ = user_voice_activ[0]


            self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM Users
            WHERE voice_activ > ? AND server_id = ?;
            """, 
            (user_voice_activ, server_id))
            
            rank = self.cursor.fetchone()[0] + 1
            if (rank > limit or member != None) and subar:
                if user_voice_activ is None or user_voice_activ == 0:
                    days, hours, minutes, seconds = 0, 0, 0, 0
                else:
                    days, hours, minutes, seconds = Member.convert_seconds(user_voice_activ)
                user = ctx.guild.get_member(user_id)
                await ctx.channel.send(embed=disnake.Embed(description=f"<@{user_id}>\n**Ваше текущее место:** {rank}\nВремя: {int(days)}д {int(hours)}ч {int(minutes)}м {int(seconds)}с\n\n", colour=self.ProfileColor).set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png?ex=66c67201&is=66c52081&hm=269a763945fef2aff03bc746e97d383b8776db4ef7c3771fd3c29b5a853cfdce&").set_thumbnail(user.avatar.url))

class LeaderTypeEnum(enum.Enum):
    Voice = 0
    
    @staticmethod
    def getClass(types : list[LeaderType], type : enum.Enum):
        for a in types:
            if a and a == type:
                return a
        return None

@Indelifer("leaders")
class Leaders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursor = Data.getCur()
        self.ProfileColor = settings.InvisibleColor
        self.types : list[LeaderType] = []
        self.types.append(LeaderVoice(self))


    @commands.slash_command()
    async def leaders(self, ctx: disnake.ApplicationCommandInteraction,  member: disnake.Member = None, subar : bool = True, limit : int = 15, type : LeaderTypeEnum = commands.Param(name="type")):
        server_id = ctx.guild.id
        user_id = ctx.author.id
        if limit > 25:
            await ctx.send(content="Max limit 25!")
            return

        if member is not None:
            user_id = member.id
        
        l = LeaderTypeEnum.getClass(self.types, type)
        if l:
            l(ctx, limit, server_id, user_id, member, subar)
        else:
            await ctx.send(embed=disnake.Embed(description="type not found", colour=self.ProfileColor))
        