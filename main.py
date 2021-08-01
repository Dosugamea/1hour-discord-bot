import discord

client = discord.Client()


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if "かわいい" in message.content:
        await message.channel.send('香風智乃のほうがかわいい')


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()

    TOKEN = os.getenv('BOT_TOKEN')
    client.run(TOKEN)
