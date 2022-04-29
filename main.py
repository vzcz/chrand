import discord
import random
import time
import os
import requests
Token = os.environ["DISCORD_BOT_TOKEN"]

client = discord.Client()

@client.event
async def on_ready():
    print('Welcome i am {0.user} how are you'. format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message}: {channel}')

    if message.author == client.user:
        return

    if user_message.lower() == '!hi':
        await message.channel.send(f'hello {str(message.author).split("#")[0]} how are you')
        return

    userList = user_message.lower().strip().split(" ")

    firstWin = len(userList) - 1
    if userList[0].lower() == '!random':
        userList.pop(0)
        lenList = len(userList) - 1
        print(lenList)
        num = 2
        try:
            for arr in range(len(userList)):
                if firstWin == len(userList):
                    indPop = random.randint(0, lenList)
                    await message.channel.send(f'1: {userList[indPop]} :confetti_ball:')
                    userList.pop(indPop)
                    lenList = lenList - 1
                time.sleep(2)
                indPop = random.randint(0, lenList)
                await message.channel.send(f'{num}: {userList[indPop]}')
                num = num+1
                userList.pop(indPop)
                lenList = lenList - 1
        except():
            return

    #wallpaper


    imageGen = message.content[7:].replace(" ", "%20")
    if userList[0].lower() == '!image':
        api_url = f'https://api.pexels.com/v1/search?query={imageGen}&per_page=5&page=1'
        print(imageGen)
        headers = {'Content-Type': 'application/json'}

        response = requests.get(api_url)

        jsontest = response.json()

    for i in range(4):
        await message.channel.send(jsontest['photos'][i]['src']['large'])





client.run(Token)