import disnake

async def addReaction(message: disnake.Message):
    if (message.channel.id == 1207418537031770172):
        await message.add_reaction("👍")
        await message.add_reaction("👎")
    if (message.channel.id == 1207777061914157166):
        await message.add_reaction("👍")
        await message.add_reaction("👎")
