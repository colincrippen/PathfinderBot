import os

import arc
import hikari
from dotenv import load_dotenv

load_dotenv()
intents = hikari.Intents.GUILD_MESSAGES | hikari.Intents.GUILD_MESSAGE_REACTIONS

bot = hikari.GatewayBot(os.getenv("BOT_TOKEN", ""), intents=intents)
client = arc.GatewayClient(bot)

client.load_extensions_from("./pathfinder_bot/extensions")
all_extensions = [
    "pathfinder_bot.extensions." + filename[:-3]
    for filename in os.listdir("./pathfinder_bot/extensions")
    if filename.endswith(".py")
]


@client.include
@arc.slash_command("reload_extensions", "Reload a specified extension, or all of them if none is given.")
async def reload_extensions(
    ctx: arc.GatewayContext,
    extensions: arc.Option[str, arc.StrParams("The extensions to reload, separated with spaces")] = "All extensions",
) -> None:
    if extensions != "All extensions":
        for extension in extensions.split(" "):
            if (extension_path := "pathfinder_bot.extensions." + extension) not in all_extensions:
                await ctx.respond(f"invalid extension name {extension}")
                return

            client.unload_extension(extension_path)
            client.load_extension(extension_path)

    else:
        for extension in all_extensions:
            client.unload_extension(extension)
            client.load_extension(extension)

    await client.resync_commands()
    await ctx.respond("Extensions reloaded!")


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
