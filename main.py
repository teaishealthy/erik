import asyncio
import inspect
import time
import traceback
from io import BytesIO
from typing import List
from urllib.parse import urlencode

from eludris.ext.commands import Context
from PIL import Image

from bot.erik import Erik
from bot.utils import codeblock, convert_to_ascii_art

bot = Erik("Erik [BOT]", prefix="erik ")


@bot.command()
async def help(ctx: Context, *commands: str):
    """Shows this message."""
    if command := " ".join(commands):
        await bot.send(inspect.getdoc(bot.commands[command]))  # type: ignore
    else:
        command_texts: List[str] = [
            f"{command} {' ' * (20 - len(command))} {bot.commands[command].__doc__}"
            for command in bot.commands
        ]

        await bot.send(codeblock("\n".join(command_texts)))


@bot.command()
async def ping(_: Context):
    """Ping the bot."""
    s = time.perf_counter()
    await bot.send("Pong!")
    e = time.perf_counter()
    await bot.send(f"Time taken: {round((e-s)*1000)}ms")


@bot.command()
async def httpcat(ctx: Context, code: int):
    """Get an HTTP cat."""
    async with bot.session.get(f"https://http.cat/{code}") as response:
        image = Image.open(BytesIO(await response.read()))
        # add codeblock
        await bot.send(
            f"<https://http.cat/{code}>\n{codeblock(convert_to_ascii_art(image))}"
        )


@bot.command()
async def calc(ctx: Context, *expressions: str):
    """Calculate an expression."""
    expression = " ".join(expressions)

    async with bot.session.get(
        f"https://api.mathjs.org/v4/?expr={urlencode({'expr': expression})}"
    ) as response:
        text = await response.text()
        if not text.startswith("Error"):
            await bot.send(text)
        else:
            await bot.send("Oh no, someone made a fucky wucky. Try again? 👉👈")

def load_commands():
    from bot.commands.games import Games
    from bot.commands.github import Github
    from bot.commands.minecraft import Minecraft
    from bot.commands.urbandict import UrbanDict

    Github(bot)
    Minecraft(bot)
    Games(bot)
    UrbanDict(bot)


async def main():
    load_commands()

    while True:
        try:
            await bot.run()
        except KeyboardInterrupt:
            break
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)

            # Something went wrong, wait 5 seconds and try again

            await bot.ws.close()
            await bot.session.close()
            await asyncio.sleep(5)
            continue


asyncio.run(main())
