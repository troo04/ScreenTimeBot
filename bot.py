import os
import time
import discord
from discord.ext.tasks import loop
from server import keep_running
client = discord.Client()

@loop(count=1)
async def send_stuff(message, secs):
    time.sleep(10)
    await message.channel.send("```It has been 10 seconds, you can take a break now\nType $stop and then $getInfo for information on how to decrease risk of neck and/or eye strain```")

@send_stuff.before_loop
async def before_send_links():
    await client.wait_until_ready()

@client.event
async def on_ready():
    print('{0.user} is online'.format(client))

@client.event
async def on_message(message):
    mins = 20
    if message.author == client.user:
        return

    if message.content == "$help":
        txt = "```The Commands of TheAllMighty include:\n$help ~ Documentation on the Screen Time bot\n$setTime,___ ~ Set the timer interval between every notification, followed by the time(mins). Example: $setTime,20\n$start ~ Starts the timer\n$stop ~ Stops the timer\n$getInfo ~ Returns information on how to prevent eye and/or neck strain```"
        await message.channel.send(txt)
    elif not message.content.find("$setTime,") == -1:
        mins = int(message.content.split(",")[1])
        await message.channel.send("You have successfully set the time interval to {} minutes".format(mins))
    elif message.content == "$start":
        txt = "```Got it! I shall remind you in 10 seconds.```"
        await message.channel.send(txt)
        while True:
            await send_stuff.start(message, mins * 60)
    elif message.content == "$stop":
        send_stuff.cancel()
        await message.channel.send("```Exited```")
    elif message.content == "$getInfo":
        txt = "```Stand up for short intervals; Make sure to take regular breaks away from the screen. Set a timer to remind you to look away every 20 minutes at an object that is about 20 feet away for a full 20 seconds.```"
        await message.channel.send(txt)

keep_running()
client.run(os.environ['TOKEN'])
