import os

import arc
import hikari
from dotenv import load_dotenv

load_dotenv()
intents = hikari.Intents.GUILD_MESSAGES | hikari.Intents.GUILD_MESSAGE_REACTIONS

bot = hikari.GatewayBot(os.getenv("BOT_TOKEN", ""), intents=intents)
client = arc.GatewayClient(bot)

client.load_extensions_from("./pathfinder_bot/extensions")


@client.include
@arc.slash_command("ping")
async def ping(ctx: arc.GatewayContext) -> None:
    await ctx.respond("Pong!")


if __name__ == "__main__":
    if os.name != "nt":
        import asyncio  # noqa: I001
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    bot.run()
