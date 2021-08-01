from discord.ext import commands  # Bot Commands Frameworkをインポート
import discord
import dataclasses
import requests
import random


@dataclasses.dataclass
class Config:
    endpoint: str
    token: str
    cdn: str


# コグとして用いるクラスを定義。
class TestCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command()
    async def chino(self, ctx):
        resp = requests.get(
            self.config.endpoint, headers={"Authorization": self.config.token}
        ).json()["data"]["imgs"]
        resp = random.choice(resp)
        embed = discord.Embed(
            title=resp["title"],
            url=resp["originUrl"],
            description=resp["artist"]["name"],
            color=0x7accff
        )
        embed.set_thumbnail(
            url=f"{self.config.cdn}/illusts/large/{resp['illustID']}.jpg"
        )
        embed.add_field(name="登録日", value=resp["date"], inline=False)
        embed.set_footer(text="Provided from Gochiira")
        await ctx.send(embed=embed)


# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class MyBot(commands.Bot):

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()

    TOKEN = os.getenv('BOT_TOKEN')
    config = Config(
        endpoint=os.getenv('GOCHIIRA_ENDPOINT'),
        token=os.getenv('GOCHIIRA_TOKEN'),
        cdn=os.getenv('GOCHIIRA_CDN')
    )
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(TestCog(bot, config))
    bot.run(TOKEN)
