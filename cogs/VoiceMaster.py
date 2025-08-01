import disnake
from disnake.ext import commands
import time 
import util.Resouces as res
from disnake import TextInputStyle
from disnake.interactions.application_command import ApplicationCommandInteraction
from util._init_ import Indelifer, CogBase

class MyModal(disnake.ui.Modal):
    def __init__(self, channel):

        self.channel: disnake.GuildChannel = channel

        components = [
            disnake.ui.TextInput(
                label="limit",
                placeholder="3",
                custom_id="countLimit",
                style=TextInputStyle.short,
                max_length=2,
            ),
        ]
        super().__init__(title="VoiceMaster", components=components)
        MyModal.logger.info("init")

    async def callback(self, inter: disnake.ModalInteraction):
            
        countLimit = inter.text_values["countLimit"]
        await self.channel.edit(user_limit=countLimit)
        await inter.send(f"Вы успешно изменили лимит на {countLimit}")

@Indelifer("voicemaster")
class VoiceMaster(CogBase):
    async def init(self):
        self.heshmap = {}
        self.metadata = res.loadJsonObject("voicemaster")

    async def updateCountMemberInVoice(self, guild: disnake.Guild, channel: disnake.VoiceChannel):
            if channel.id in self.heshmap:
                self.heshmap[channel.id]["countMember"] = len(channel.members)
                if self.heshmap[channel.id]["countMember"] <= 0:
                    voice_channel = guild.get_channel(self.heshmap[channel.id]["channelId"])
                    if voice_channel:
                        await voice_channel.delete()
                    del self.heshmap[channel.id]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before, after):
        guild: disnake.Guild = member.guild
        category = disnake.utils.get(guild.categories, id=self.metadata.category)

        if before.channel is None and after.channel is not None:
            self.logger.debug(str(self.heshmap))

            if after.channel.id == self.metadata.channel: 
                channel: disnake.VoiceChannel = await guild.create_voice_channel(name=member.name, category=category)
                self.heshmap[channel.id] = {
                    "channelId": channel.id,
                    "owner": member.id,
                    "countMember": 1,
                    "timeOutName": 0,
                    "timeOutLimit": 0
                }
                await member.move_to(channel=channel)

        elif before.channel is not None and after.channel is None:
            self.logger.debug(str(self.heshmap))
 
            if before.channel.id in self.heshmap:
                await self.updateCountMemberInVoice(guild, before.channel)

        elif before.channel != after.channel:
            self.logger.debug(str(self.heshmap))

            if after.channel.id == self.metadata.channel: 
                channel: disnake.VoiceChannel = await guild.create_voice_channel(name=member.name, category=category)
                self.heshmap[channel.id] = {
                    "channelId": channel.id,
                    "owner": member.id,
                    "countMember": 1,
                    "timeOutName": 0,
                    "timeOutLimit": 0
                }
                await member.move_to(channel=channel)

            if before.channel and before.channel.id in self.heshmap:
                await self.updateCountMemberInVoice(guild, before.channel)

            if after.channel and after.channel.id in self.heshmap:
                await self.updateCountMemberInVoice(guild, after.channel)

    @commands.command()
    async def panel(self, ctx: ApplicationCommandInteraction):
        embed = disnake.Embed(description="### Управление приватной комнатой")
        
        components = [disnake.ui.Button(label="", style = disnake.ButtonStyle.grey, custom_id="loock", emoji="🔒"), disnake.ui.Button(label="", style = disnake.ButtonStyle.grey, custom_id="view", emoji="👁️"), disnake.ui.Button(label="", style = disnake.ButtonStyle.grey, custom_id="limit", emoji="👥"), disnake.ui.Button(label="", style = disnake.ButtonStyle.grey, custom_id="renject", emoji="❌")]
        await ctx.send(embed=embed, components=components)

    @commands.Cog.listener(disnake.Event.button_click)
    async def button_click(self, inter: disnake.MessageInteraction):
        if (inter.component.custom_id == "loock"):
            idChannel = inter.author.voice.channel.id
            if idChannel in self.heshmap:
                if (self.heshmap[idChannel]["owner"] == inter.author.id):
                    channel = inter.author.guild.get_channel(idChannel)
                    everyone_perms = channel.overwrites_for(inter.guild.default_role)

                    if (everyone_perms.connect is None or everyone_perms.connect is True):
                        overwrite = disnake.PermissionOverwrite(connect=False)
                        overwrite1 = disnake.PermissionOverwrite(connect=True)
                        await channel.set_permissions(inter.guild.get_member(inter.author.id), overwrite=overwrite1)
                        await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
                        embed = disnake.Embed(description="Вы успещно закрывли канал.")
                    else: 
                        overwrite = disnake.PermissionOverwrite(connect=True)
                        overwrite1 = disnake.PermissionOverwrite(connect=True)
                        await channel.set_permissions(inter.guild.get_member(inter.author.id), overwrite=overwrite1)
                        await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
                        embed = disnake.Embed(description="Вы успещно открыли канал.")

                    await inter.send(embed=embed, ephemeral=True)
            else: 
                embed = disnake.Embed(description="У тебя нету прав.")
                await inter.send(embed=embed, ephemeral=True)

        if (inter.component.custom_id == "limit"):
                idChannel = inter.author.voice.channel.id
                channel: disnake.GuildChannel = inter.author.guild.get_channel(idChannel)
                if idChannel in self.heshmap:
                    if (self.heshmap[idChannel]["owner"] == inter.author.id):
                        await inter.response.send_modal(modal=MyModal(channel))
                else:
                    embed = disnake.Embed(description="У тебя нету прав.")
                    await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="voice_lock")
    async def lock(self, inter: ApplicationCommandInteraction):
        idChannel = inter.author.voice.channel.id
        if idChannel in self.heshmap:
            if (self.heshmap[idChannel]["owner"] == inter.author.id):
                channel = inter.author.guild.get_channel(idChannel)
                everyone_perms = channel.overwrites_for(inter.guild.default_role)

                if (everyone_perms.connect is None or everyone_perms.connect is True):
                    overwrite = disnake.PermissionOverwrite(connect=False)
                    overwrite1 = disnake.PermissionOverwrite(connect=True)
                    await channel.set_permissions(inter.guild.get_member(inter.author.id), overwrite=overwrite1)
                    await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
                    embed = disnake.Embed(description="Вы успещно закрывли канал.")
                else: 
                    overwrite = disnake.PermissionOverwrite(connect=True)
                    overwrite1 = disnake.PermissionOverwrite(connect=True)
                    await channel.set_permissions(inter.guild.get_member(inter.author.id), overwrite=overwrite1)
                    await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
                    embed = disnake.Embed(description="Вы успещно открыли канал.")

                await inter.send(embed=embed, ephemeral=True)
        else:
            await inter.send("Канал не найден.")

    @commands.slash_command(name="voice_view")
    async def view(self, inter: ApplicationCommandInteraction):
        idChannel = inter.author.voice.channel.id
        if idChannel in self.heshmap:
            if (self.heshmap[idChannel]["owner"] == inter.author.id):
                channel = inter.author.guild.get_channel(idChannel)
                everyone_perms = channel.overwrites_for(inter.guild.default_role)

                if (everyone_perms.connect is None or everyone_perms.connect is True):
                    overwrite = disnake.PermissionOverwrite(view=False)
                    overwrite1 = disnake.PermissionOverwrite(view=True)
                    await channel.set_permissions(inter.guild.get_member(inter.author.id), overwrite=overwrite1)
                    await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
                    embed = disnake.Embed(description="Ваш канал не видно.")
                else: 
                    overwrite = disnake.PermissionOverwrite(view=True)
                    overwrite1 = disnake.PermissionOverwrite(view=True)
                    await channel.set_permissions(inter.guild.get_member(inter.author.id), overwrite=overwrite1)
                    await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
                    embed = disnake.Embed(description="Ваш канал видно.")

                await inter.send(embed=embed, ephemeral=True)
        else: 
            embed = disnake.Embed(description="У тебя нету прав.")
            await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="voice_limit")
    async def limit(self, inter: ApplicationCommandInteraction, limit: int):
        idChannel = inter.author.voice.channel.id
        channel: disnake.GuildChannel = inter.author.guild.get_channel(idChannel)
        
        if idChannel in self.heshmap:
            if self.heshmap[idChannel]["owner"] == inter.author.id:
                if self.heshmap[idChannel]["timeOutLimit"] == 0 or self.heshmap[idChannel]["timeOutLimit"] < time.time():
                    if limit <= 99:
                        await channel.edit(user_limit=limit)
                        await inter.send(f"Вы успешно изменили лимит на {limit}")
                        self.heshmap[idChannel]["timeOutLimit"] = time.time() + 120
                    else:
                        await inter.send(f"Вы не можете превышать лимит")
                else:
                    remaining_time = int(self.heshmap[idChannel]["timeOutLimit"] - time.time())
                    await inter.send(f"Вы не можете изменить лимит сейчас. Подождите {remaining_time} секунд.")
            else:
                await inter.send("У тебя нет прав для изменения лимита.")
        else:
            await inter.send("Канал не найден.")


    @commands.slash_command(name="voice_reject")
    async def reject(self, inter: ApplicationCommandInteraction, member: disnake.Member):
        idChannel = inter.author.voice.channel.id
        channel: disnake.GuildChannel = inter.author.guild.get_channel(idChannel)
        if idChannel in self.heshmap:
            if (self.heshmap[idChannel]["owner"] == inter.author.id):
                await channel.set_permissions(member, overwrite=disnake.PermissionOverwrite(connect=False))
                if member.voice and member.voice.channel and member.voice.channel.id == idChannel:
                    await member.edit(voice_channel=None)
            else:
                await inter.send("У тебя нет прав.")
        else:
            await inter.send("Канал не найден.")

    @commands.slash_command(name="voice_permit")
    async def permit(self, inter: ApplicationCommandInteraction, member: disnake.Member):
        idChannel = inter.author.voice.channel.id
        channel: disnake.GuildChannel = inter.author.guild.get_channel(idChannel)
        if idChannel in self.heshmap:
            if (self.heshmap[idChannel]["owner"] == inter.author.id):
                await channel.set_permissions(member, overwrite=disnake.PermissionOverwrite(connect=True))
            else:
                await inter.send("У тебя нет прав.")
        else:
            await inter.send("Канал не найден.")

    @commands.slash_command(name="voice_claim")
    async def claim(self, inter: ApplicationCommandInteraction):
        idChannel = inter.author.voice.channel.id
        channel: disnake.GuildChannel = inter.author.guild.get_channel(idChannel)
        if idChannel in self.heshmap:
            if (inter.guild.get_member(self.heshmap[idChannel]["owner"]).voice):
                embed = disnake.Embed(description="Владелиц войса находится в этом канале.")
            else: 
                self.heshmap[idChannel]["owner"] = inter.author.id
                embed = disnake.Embed(description="Вы успешно забрали канал теперь вы новый владлиц.")

            await inter.send(embed=embed)
        else:
            await inter.send("Канал не найден.")

    @commands.slash_command(name="voice_name")
    async def name(self, inter: ApplicationCommandInteraction, name: str):
        idChannel = inter.author.voice.channel.id
        channel: disnake.GuildChannel = inter.author.guild.get_channel(idChannel)
        if idChannel in self.heshmap:
            if (self.heshmap[idChannel]["owner"] == inter.author.id):
                if self.heshmap[idChannel]["timeOutName"] == 0 or self.heshmap[idChannel]["timeOutName"] < time.time():
                    await channel.edit(name=name)
                    self.heshmap[idChannel]["timeOutName"] = time.time() + 120
                    embed = disnake.Embed(description=f"Вы успешно изменили названия канала на {name}.")
                    await inter.send(embed=embed)
                else:
                    remaining_time = int(self.heshmap[idChannel]["timeOutName"] - time.time())
                    await inter.send(f"Вы не можете изменить названия сейчас. Подождите {remaining_time} секунд.")
            else:
                await inter.send("У тебя нет прав для изменения лимита.")
        else:
            await inter.send("Канал не найден.")
