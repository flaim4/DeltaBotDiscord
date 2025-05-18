from util.event import bus, OnMessage

async def addReaction(event: OnMessage):
    message = event.message
    
    if (message.channel.id == 1207418537031770172):
        await message.add_reaction("👍")
        await message.add_reaction("👎")
    if (message.channel.id == 1207777061914157166):
        await message.add_reaction("👍")
        await message.add_reaction("👎")


bus.subscribe(OnMessage, addReaction)