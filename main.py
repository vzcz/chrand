import discord
import random
import time
import os
import requests

Token = os.environ["DISCORD_BOT_TOKEN"]
api_token = os.environ["IMAGE_API_TOKEN"]

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


    if userList[0].lower() == '!image':
        numImage = 5
        try:
            lenNum = len(userList[1])
            numImage = int(userList[1])
            imageGen = message.content[8 + lenNum:].replace(" ", "%20")
            api_url = f'https://api.pexels.com/v1/search?query={imageGen}&per_page={numImage}&page=1'
        except:
            imageGen = message.content[7:].replace(" ", "%20")
            api_url = f'https://api.pexels.com/v1/search?query={imageGen}&per_page=5&page=1'
        header = {'Content-Type': 'application/json',
                  'Authorization': api_token}

        response = requests.get(api_url, headers=header)

        jsontest = response.json()

        for i in range(numImage):
            await message.channel.send(jsontest['photos'][i]['src']['large'])

    if user_message == '!!help':
        embed = discord.Embed(
            colour= discord.Colour.random()
        )
        embed.set_author(name="Help")
        embed.add_field(name='!random <select> <select> <select> <select>', value="Random selection\nEx: !random ali ahmad saad khalid", inline=False)
        embed.add_field(name='!image <number of images> <image name>', value='Gives you a set of photos (the number of photos is optional)\nEx: !image 2 sky', inline=False)
        embed.add_field(name='!proxy <type>', value='Generate free proxy for different types \ntypes:\nhttp\nsock4\nsock5\nEx: !proxy http', inline=False)
        await message.channel.send(embed=embed)

    if userList[0].lower() == '!proxy':
        try:
            # Choose the type of proxy
            if userList[1].lower() == "socks5":
                prx_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all"
                typePrx = "socks5"
            elif userList[1].lower() == "socks4":
                prx_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all"
                typePrx = "socks4"
            elif userList[1].lower() == "http":
                prx_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
                typePrx = "HTTP"

            res = requests.get(prx_url)

            #
            if "502 Bad Gateway" in res.text or "Error 543" in res.text:
                await message.channel.send("Wait a moment, then try again there are some problems")
            else:
                await message.channel.send(typePrx)
                filePrx = open("resprox.txt", "w")
                result = res.text.replace("\n", " ")
                filePrx.write(result)
                filePrx.close()
                await message.channel.send(file=discord.File('resprox.txt'))


        except:

            if len(userList) == 1:
                await message.channel.send("Please enter proxy type")
            elif userList[1].lower() != "http" or userList[1].lower() != "socks5" or userList[1].lower() != "socks4":
                await message.channel.send("Incorrect type")
            else:
                await message.channel.send("Wait a minute, there are some problems")


client.run(Token)
