import json
from typing import Any, TypeVar

import arc
import hikari

from . import ATTRIBUTE_NAMES, CLASS_LIST, PROFICIENCY_NAMES

plugin = arc.GatewayPlugin("classes")

T = TypeVar("T")

"""
type System = dict[
    str,
    int
    | list
    | dict[str, list[int]]
    | dict[str, int | dict[str, str | int]]
    | dict[str, int]
    | dict[str, str]
    | dict[str, dict[str, str | int]]
    | dict[str, list[str]]
    | dict[str, str | bool]
    | dict[str, int | str | list[str]]
    | dict[str, str | list],
]
"""


def format_class_data(data: dict[str, Any]) -> dict[str, Any]:
    output_dict: dict[str, Any] = data["system"]
    output_dict["name"] = data["name"]
    # strip all the empty "value" dicts
    for k, v in output_dict.items():
        if isinstance(v, dict) and len(v) == 1:
            output_dict[k] = v["value"]

    # TODO: actually handle items
    output_dict.pop("items")

    desc: str = output_dict["description"]
    end_index: int = desc.find("</em></p>")
    output_dict["description"] = desc[7:end_index]

    return output_dict


def get_class_embed(data: dict) -> hikari.Embed:
    embed = hikari.Embed(
        title=data["name"],
        description=f"*{data['description']}*\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        colour=0x00B000,
    )

    key_attribute: str
    if len(key_attr_list := data["keyAbility"]) == 1:
        key_attribute = ATTRIBUTE_NAMES[key_attr_list[0]]
    else:
        key_attribute = " or ".join(ATTRIBUTE_NAMES[i] for i in key_attr_list)

    embed.add_field(name="Key Attribute", value=f"{key_attribute}", inline=True)
    embed.add_field(name="Hit Points", value=f"{data['hp']} plus your Constitution modifier", inline=True)
    embed.add_field(name=".", value="⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯", inline=False)
    embed.add_field(name="Perception", value=f"{PROFICIENCY_NAMES[data['perception']]} in Perception", inline=True)

    embed.add_field(
        name="Saving Throws",
        value=f"{PROFICIENCY_NAMES[data['savingThrows']['fortitude']]} in Fortitude\n{PROFICIENCY_NAMES[data['savingThrows']['reflex']]} in Reflex\n{PROFICIENCY_NAMES[data['savingThrows']['will']]} in Will",
        inline=True,
    )
    embed.add_field(
        name="Skills",
        # value=f"Trained in {data['trainedSkills']['value'][0].capitalize()}\nTrained in a number of additional skills equal to {data['trainedSkills']['additional']} plus your Intelligence modifier",
        value="temp, fix later",
        inline=True,
    )
    embed.add_field(
        name="Attacks",
        value=f"{PROFICIENCY_NAMES[data['attacks']['simple']]} in simple weapons\n{PROFICIENCY_NAMES[data['attacks']['martial']]} in martial weapons\n{PROFICIENCY_NAMES[data['attacks']['advanced']]} in advanced weapons\n{'Untrained'} in other\n{PROFICIENCY_NAMES[data['attacks']['unarmed']]} in unarmed attacks",
        inline=True,
    )
    embed.add_field(
        name="Defenses",
        value=f"{PROFICIENCY_NAMES[data['defenses']['light']]} in light armor\n{PROFICIENCY_NAMES[data['defenses']['medium']]} in medium armor\n{PROFICIENCY_NAMES[data['defenses']['heavy']]} in heavy armor\n{PROFICIENCY_NAMES[data['defenses']['unarmored']]} in unarmored defense",
        inline=True,
    )

    return embed


@plugin.include
@arc.slash_command("class", "Get information about a class.")
async def get_class(
    ctx: arc.GatewayContext,
    class_path: arc.Option[str, arc.StrParams(description="The class", name="class", choices=CLASS_LIST)],
) -> None:
    with open(class_path, "r") as file:
        class_json: dict[str, Any] = json.load(file)

    class_json = format_class_data(class_json)
    response_embed: hikari.Embed = get_class_embed(class_json)

    await ctx.respond(response_embed)


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)


@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
