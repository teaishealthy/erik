import asyncio
import random
import time
from eludris import Message
import mcstatus

from eludris.ext.commands import Bot, Context


    

bot = Bot("Erik [BOT]", prefix="erik ")


@bot.command()
async def imposter(ctx: Context, user: str, *message: str):
    original = bot.name
    try:
        bot.name = user
        await bot.send(" ".join(message))
    finally:
        bot.name = original

@bot.command()
async def ping(_: Context):
    s = time.perf_counter()
    await bot.send(f"Pong!")
    e = time.perf_counter()
    await bot.send(f"Time taken: {round((e-s)*1000)}ms")

@bot.command()
async def rps(ctx: Context):
    await bot.send("Rock, paper, scissors")
    choice = random.choice(["rock", "paper", "scissors"])
    message = await bot.wait_for_message(ctx.author)
    if message.content.lower() == "rock":
        if choice == "rock":
            await bot.send(f"I chose {choice}. Tie! @{message.author} ")
        elif choice == "paper":
            await bot.send(f"I chose {choice}. I win! @{message.author} ")
        elif choice == "scissors":
            await bot.send(f"I chose {choice}. You win! @{message.author} ")
    elif message.content.lower() == "paper":
        if choice == "rock":
            await bot.send(f"I chose {choice}. You win! @{message.author} ")
        elif choice == "paper":
            await bot.send(f"I chose {choice}. Tie! @{message.author} ")
        elif choice == "scissors":
            await bot.send(f"I chose {choice}. I win! @{message.author} ")
    elif message.content.lower() == "scissors":
        if choice == "rock":
            await bot.send(f"I chose {choice}. I win! @{message.author} ")
        elif choice == "paper":
            await bot.send(f"I chose {choice}. You win! @{message.author} ")
        elif choice == "scissors":
            await bot.send(f"I chose {choice}. Tie! @{message.author} ")

@bot.command(name="dad joke")
async def dadjoke(_: Context):
    async with bot.session.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"}) as response:
        data = await response.json()
        await bot.send(data["joke"])

@bot.command(name="github repo")
async def github(ctx: Context, *repo):
    # Get info about repo from github
    repo = "/".join(repo)
    async with bot.session.get(f"https://api.github.com/repos/{repo}") as response:
        data = await response.json()
        await bot.send(f"{data['name']} - {data['description']}")

@bot.command(name="mc server")
async def mcserver(ctx: Context, server_ip: str):
    server = await mcstatus.JavaServer.async_lookup(server_ip)
    status = await server.async_status()

    await bot.send(f"{server_ip} - {status.players.online}/{status.players.max} players")
    await bot.send(f"{status.version.name} - {round(status.latency)}ms")

@bot.command(name="ud")
async def urban_dictionary(ctx: Context, term: str):
    async with bot.session.get(f"https://api.urbandictionary.com/v0/define?term={term}") as response:
        data = await response.json()
        if data["list"]:
            for i in data["list"][0]["definition"].split("\n"):
                await bot.send(i.strip())
        else:
            await bot.send("No results")

@bot.command(name="rename")
async def rename(ctx: Context, *name: str):
    bot.name = " ".join(name)
    await bot.send(f"Renamed!")
    await asyncio.sleep(5)
    bot.name = "Erik [BOT]"
    await bot.send(f"Back to Erik!")



async def main():
    while True:
        try:
            await bot.run()
        except KeyboardInterrupt:
            break
        except Exception as e:
            await bot.ws.close()
            await bot.session.close()
            print("Eludris fucking crashed. Again.\nRestarting. Again.")
            await asyncio.sleep(5)
            continue

asyncio.run(main())
