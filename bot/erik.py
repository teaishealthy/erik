from typing import Any

from eludris.ext.commands import Bot


class Erik(Bot):
    def add_command(self, name: str, command: Any):
        self.command(name)(command)
