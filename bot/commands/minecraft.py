import mcstatus
from eludris.ext.commands import Context

from bot.erik import Erik


class Minecraft:
    def __init__(self, bot: Erik):
        self.bot = bot
        bot.add_command("mc server", self.minecraft_server)

    async def minecraft_server(self, ctx: Context, server_ip: str):
        """Get info about a minecraft server."""
        server = await mcstatus.JavaServer.async_lookup(server_ip)
        status = await server.async_status()  # type: ignore

        await self.bot.send(
            f"{server_ip} - {status.players.online}/{status.players.max} players\n"
            f"{status.version.name} - {round(status.latency)}ms"
        )
