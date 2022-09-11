from eludris.ext.commands import Context

from bot.erik import Erik


class Github:
    def __init__(self, bot: Erik):
        self.bot = bot
        bot.add_command("github repo", self.github)

    async def github(self, ctx: Context, *repo: str):
        """Get a github repo."""
        # Get info about repo from github
        repo_name = "/".join(repo)
        async with self.bot.session.get(
            f"https://api.github.com/repos/{repo_name}"
        ) as response:
            data = await response.json()
            if response.status == 404:
                await self.bot.send(f"Repo {repo_name} not found. Fucking idiot.")
                return
            desc = " - " + data["description"] or ""
            await self.bot.send(
                f"{repo_name}{desc}\n"
                f"https://github.com/{repo_name}\n"
                f"{data['stargazers_count']} Stars, {data['forks_count']} Forks, {data['open_issues_count']} Issues\n"
            )
