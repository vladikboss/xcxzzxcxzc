import discord
import aiohttp
import asyncio

from bs4 import BeautifulSoup
from discord.ext import tasks, commands

from config_loader import load_config


class SendOnlineCog(commands.Cog):
    """
    This cog parsing GM server current online and sending it to the discord channel every 5 minutes.
    """
    def __init__(self, bot):
        self.bot = bot
        self.link = load_config().get("link")  # Link to the game server, format [https://tsarvar.com/ru/servers/garrys-mod/SERVER_IP]
        self.channel_id = load_config().get("bot_channel_ID")  # Channel for sending bot messages about server online.
        self.message = None
        self.send_online.start()  # Starting task with parsing.

    @tasks.loop()
    async def send_online(self):
        """
        This method parsing server online from `tsarvar.com`
        and sends it to the channel every 5 minutes.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.link) as response:
                print(f"\n============================\nУспешно. взял данные (online)")

                html = await response.text()  # Parse HTML markup from response.
                soup = BeautifulSoup(html, "html.parser")

                cur_online = soup.find("span", class_="srvPage-countCur")  # Get current online.
                max_online = soup.find("span", class_="srvPage-countMax")  # Get max online.
                ip_server = soup.find("span", class_="srvPage-addrText")  # Get ip server.

                embed = discord.Embed(  # Create embed message with current and max online.
                    title="[ZTK Приватный сервер]:\n`Версия 1.16.5`",
                    description=f"[**Онлайн:** `{cur_online.text} / {max_online.text}`] [**Айпи:** `{ip_server.text}`]\n```Данные обновляются каждые 5-минут```",
                    colour=int("0x2f3136", 16)
                )
                embed.set_thumbnail(url="http://images.vfl.ru/ii/1641759214/84e0d592/37456171_m.png")
                if self.message is None:
                    channel = self.bot.get_channel(self.channel_id)
                    self.message = await channel.send(embed=embed)  # Send message with online.

                else:
                    try:
                        await self.message.edit(embed=embed)
                    except:
                        self.message = None

        await asyncio.sleep(60)  # Wait 5 minutes.


def setup(bot):
    bot.add_cog(SendOnlineCog(bot))
