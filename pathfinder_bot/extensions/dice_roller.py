import random

import arc

plugin = arc.GatewayPlugin("dice_roller")


@plugin.include
@arc.slash_command("roll", description="Roll a die of arbitrary size", is_dm_enabled=False)
async def roll(
    ctx: arc.GatewayContext,
    size: arc.Option[int, arc.IntParams(description="The size of the die", choices=[2, 4, 6, 8, 10, 12, 20])] = 20,
) -> None:
    roll = random.randint(1, size)
    await ctx.respond(f"1d{size} = {roll}")


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)


@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
