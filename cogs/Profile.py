import disnake 
from disnake.ext import commands
import settings
from util.member import Member
from util.balance import Balance
from util._init_ import Indelifer, CogBase

from disnake.interactions.application_command import ApplicationCommandInteraction

@Indelifer("profile")
class Profile(CogBase):
    @commands.slash_command(description="Посмотреть профиль")
    async def profile(self, ctx, member: disnake.Member = None):
        
        await ctx.response.defer()

        if ctx.author.bot:
            return
        
        if member is None:
            member = ctx.author

        if member.bot:
            await ctx.send("Профиль бота нельзя смотреть", ephemeral=True)
            return
        
        # if (Member.getLoveMember(member.guild.id, member.id) is None):
        #     components = [disnake.ui.Button(label="Открыть любовный профиль", style=disnake.ButtonStyle.blurple, custom_id="love", disabled=True)]
        # else:
        #     components = [disnake.ui.Button(label="Открыть любовный профиль", style=disnake.ButtonStyle.blurple, custom_id="love", disabled=False)]

        name=member.display_name
        server = ctx.guild

        voice_seconds = await Member.getCountSecondVoice(member.guild.id, member.id)
        
        if voice_seconds is None or voice_seconds == 0:
            days, hours, minutes, seconds = 0, 0, 0, 0
        else:
            days, hours, minutes, seconds = Member.convert_seconds(voice_seconds)

        ProfileColor = settings.InvisibleColor
        ErrorColor = settings.ErrorColor
        
        embed = disnake.Embed(description=f"### Профиль — {member.global_name}", colour=ProfileColor)
        
        activities = member.activities
        custom_status = next((activity for activity in activities if isinstance(activity, disnake.CustomActivity)), None)
        if custom_status and custom_status.name:
            embed.add_field(name="<:Edit_fill:1281281277688942724> Статус", value=f"```{custom_status.name}```", inline=False)
        else:
            embed.add_field(name="<:Edit_fill:1281281277688942724> Статус", value=f"```Статус не установлен.```", inline=False)
        embed.add_field(name="<:Hourglass_fill:1281278042978910208> Активность", value=f"```{int(days)}д, {int(hours)}ч, {int(minutes)}м```", inline=False)
        embed.add_field(name="<:Subtract1:1281279082537156618> Уровень", value=f"```{await Member.getLevelMember(member.guild, member)}```", inline=True)
        embed.add_field(name="<:Wallet_fill:1281280768919998535> Монеты", value=f"```{await Balance.getBalance(member.guild.id, member.id)}```", inline=True)
        embed.add_field(name="<:comment_fill:1281279319402090647> Сообщение", value=f"```{await Member.getCountMessage(member.guild.id, member.id)}```", inline=True)
        embed.set_thumbnail(url=member.avatar)
        await ctx.send(embed=embed) 
        #               components=[
        #    disnake.ui.Button(
        #        label="Ежедневная награда",
        #        style=disnake.ButtonStyle.secondary,
        #        custom_id="day"
        #    )
        #])


    @commands.slash_command(description="Узнать баланс")
    @commands.default_member_permissions(administrator=True)
    async def balance(self, ctx):
        await ctx.send(await Balance.getBalance(ctx.guild.id, ctx.author.id))

    @commands.slash_command(description="Добавить монеты")
    @commands.default_member_permissions(administrator=True)
    async def addbalance(self, ctx, member: disnake.Member = None, count: int = 0):
        await Balance.addBalance(ctx.guild.id, member.id, count)

    @commands.slash_command(description="Установить монеты")
    @commands.default_member_permissions(administrator=True)
    async def setbalance(self, ctx, member: disnake.Member = None, count: int = 0):
        await Balance.setBalance(ctx.guild.id, member.id, count)

    @commands.slash_command(description="Забрать монеты")
    @commands.default_member_permissions(administrator=True)
    async def spendbalance(self, ctx, member: disnake.Member = None, count: int = 0):
        await Balance.spendBalance(ctx.guild.id, member.id, count)

    @commands.slash_command(description="")
    async def pay(self, ctx: ApplicationCommandInteraction, member: disnake.Member, count: int):
        if (member.id == ctx.author.id):
            await ctx.send("Атя тя", ephemeral=True)
            return
        if (count <= 0):
            await ctx.send("Меньше нельзя!", ephemeral=True)
            return
        if Balance.getBalance(ctx.guild.id, ctx.author.id) < count:
            await ctx.send("У вас нету денег?", ephemeral=True)
            return
            
        await Balance.spendBalance(ctx.guild.id, ctx.author.id, count)
        await Balance.addBalance(ctx.guild.id, member.id, count)
        await ctx.send(f"Вы успешно перевели деньги пользователю <@{member.id}> {count} монет!")

        embed = disnake.Embed(description=f"<@{ctx.author.id}> перевел <@{member.id}> `{count}` монет", timestamp=disnake.utils.utcnow())

        embed.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.display_avatar.url}")
        
        if self.bot.get_channel(1340822278346379284) is not None:
            await self.bot.get_channel(1340822278346379284).send(embed=embed)


    # @commands.Cog.listener(disnake.Event.button_click)
    # async def button_click(self, inter: disnake.MessageInteraction):
    #     if (inter.component.custom_id == "love"):
    #         embed = disnake.Embed(description=f"### Любовный профиль — {inter.author.global_name}")
    #         love_member = inter.guild.get_member(Member.getLoveMember(inter.guild.id, inter.author.id))
    #         embed.add_field(name = "> Партнер", value = f"```{love_member.global_name}```", inline=False)
    #         current_datetime = datetime.fromtimestamp(Member.getLoveMemberDataRegister(inter.guild.id, inter.user))
    #         formatted_time = current_datetime.strftime('%Y-%m-%d')
    #         embed.add_field(name = "> Регистрация", value = f"```{formatted_time}```", inline=True)

    #         voice_seconds = time.time() - Member.getLoveMemberDataRegister(inter.guild.id, inter.user)
        
    #         if voice_seconds is None or voice_seconds == 0:
    #             days, hours, minutes, seconds = 0, 0, 0, 0
    #         else:
    #             days, hours, minutes, seconds = Member.convert_seconds(voice_seconds)

    #         embed.add_field(name = "> Всего вместе", value = f"```{int(days)}д {int(hours)}ч, {int(minutes)}м  ```", inline=True)
    #         embed.add_field(name = "> Времени проведено в любовной комнате", value = f"```{Member.getLoveMemberTimeVoice(inter.guild.id, inter.user)}```", inline=False)
    #         embed.set_thumbnail(url=inter.author.avatar.url)
    #         ProfileColor = settings.InvisibleColor
    #         embed.color = ProfileColor
    #         await inter.send(embed=embed)