import random

from eludris.ext.commands import Context

from bot.erik import Erik


class Games:
    def __init__(self, bot: Erik):
        self.bot = bot
        bot.add_command("rps", self.rps)
        bot.add_command("dad joke", self.dadjoke)
        bot.add_command("imposter", self.imposter)

    async def rps(self, ctx: Context):
        """Play rock paper scissors with the bot."""
        await self.bot.send("Rock, paper, scissors")
        choice = random.choice(["rock", "paper", "scissors"])
        message = await self.bot.wait_for_message(ctx.author)
        if message.content.lower() == "rock":
            if choice == "rock":
                await self.bot.send(f"I chose {choice}. Tie! @{message.author} ")
            elif choice == "paper":
                await self.bot.send(f"I chose {choice}. I win! @{message.author} ")
            elif choice == "scissors":
                await self.bot.send(f"I chose {choice}. You win! @{message.author} ")
        elif message.content.lower() == "paper":
            if choice == "rock":
                await self.bot.send(f"I chose {choice}. You win! @{message.author} ")
            elif choice == "paper":
                await self.bot.send(f"I chose {choice}. Tie! @{message.author} ")
            elif choice == "scissors":
                await self.bot.send(f"I chose {choice}. I win! @{message.author} ")
        elif message.content.lower() == "scissors":
            if choice == "rock":
                await self.bot.send(f"I chose {choice}. I win! @{message.author} ")
            elif choice == "paper":
                await self.bot.send(f"I chose {choice}. You win! @{message.author} ")
            elif choice == "scissors":
                await self.bot.send(f"I chose {choice}. Tie! @{message.author} ")

    async def dadjoke(self, _: Context):
        """Get a dad joke."""
        async with self.bot.session.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        ) as response:
            data = await response.json()
            await self.bot.send(data["joke"])

    async def imposter(self, ctx: Context, user: str, *message: str):
        """Send a message as another user. Suspicious."""
        original = self.bot.name
        try:
            self.bot.name = user
            await self.bot.send(" ".join(message))
        finally:
            self.bot.name = original
