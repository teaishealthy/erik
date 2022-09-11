from eludris.ext.commands import Context

from bot.erik import Erik


class UrbanDict:
    def __init__(self, bot: Erik):
        self.bot = bot
        bot.add_command("ud", self.urban_dictionary)

    async def urban_dictionary(self, ctx: Context, term: str):
        """Get a definition from urban dictionary."""
        async with self.bot.session.get(
            f"https://api.urbandictionary.com/v0/define?term={term}"
        ) as response:
            data = await response.json()
            if data["list"]:
                await self.bot.send(
                    data["list"][0]["definition"].replace("[", "").replace("]", "")
                )
            else:
                await self.bot.send("No results")
