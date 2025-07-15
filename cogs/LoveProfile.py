import disnake
from disnake.ext import commands  
from util.member import Member
import settings
from util._init_ import Indelifer, CogBase

ProfileColor = settings.InvisibleColor

@Indelifer("loveprofile")
class LoveProfile(CogBase):
    async def init(self):
        self.hesmap = {}

    @commands.slash_command()
    async def marry(self, ctx, member: disnake.Member):
        if (member.id != ctx.author.id):
            embed = disnake.Embed(description=f"### Заключение брака\n {member.mention}, Вы согласны вступить в брак с {ctx.author.mention}?", color=ProfileColor)
            components = [
                disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yes"),
                disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no")
            ]
            await ctx.send(embed=embed, components=components)
            msg = await ctx.original_message()
            self.hesmap[msg.id] = {"msg": msg, "author": ctx.author, "love": member}
        else: 
            await ctx.send("Вы не можете пригласить себя в брак!", ephemeral=True)
        

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "yes":
            for msg_id, data in self.hesmap.items():
                if inter.message.id == msg_id:
                    if inter.author.id == data["love"].id:
                        components = [
                            disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yes", disabled=True),
                            disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no", disabled=True)
                        ]
                        await data["msg"].edit(components=components)
                        await inter.send("Поздравляю!", ephemeral=True)
                        Member.setLoveMember(inter.guild.id, data["author"], data["love"])
                    else:
                        await inter.send(content="Вы не можете заключить брак! Это предложение было адресовано не вам!", ephemeral=True)

        if inter.component.custom_id == "no":
            for msg_id, data in self.hesmap.items():
                if inter.message.id == msg_id:
                    if inter.author.id == data["love"]:
                        components = [
                            disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yes", disabled=True),
                            disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no", disabled=True)
                        ]
                        await data["msg"].edit(components=components)
                        await inter.send("ОК", ephemeral=True)
                    else: 
                        await inter.send(content="Вы не можете заключить брак! Это предложение было адресовано не вам!", ephemeral=True)