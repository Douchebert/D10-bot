import discord
import os
import random

my_secret = os.environ['D10Auth']
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('!r') or message.content.startswith('!roll'):
        # Split the message content into command and arguments
        if message.content.startswith('!r'):
            _, *args = message.content.split()
        else:
            _, _, *args = message.content.split()

        # Check if there are enough arguments
        if len(args) < 2:
            await message.channel.send("Usage: !roll [dice pool] [target value]")
            return

        # Parse the arguments
        try:
            dice_pool = int(args[0])
            target_value = int(args[1])
        except ValueError:
            await message.channel.send("Usage: !roll [dice pool] [target value]")
            return

        # Roll the dice and count the result
        rolls = [random.randint(1, 10) for _ in range(dice_pool)]
        count10 = rolls.count(10)
        count = sum(1 for roll in rolls if roll >= target_value)
        count -= rolls.count(1)

        # Add the count of 10's to the total count
        if count < count10:
            count = count10

        # Send a message with the result
        if count < 0:
            await message.channel.send(f"You rolled {rolls}, and got {count} successes. You botched!")
        else:
            await message.channel.send(f"You rolled {rolls}, and got {count} successes.")

client.run(my_secret)