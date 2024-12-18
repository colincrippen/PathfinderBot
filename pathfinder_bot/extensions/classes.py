import json
from typing import Any, TypeVar

import arc

from . import CLASS_LIST

plugin = arc.GatewayPlugin("classes")

T = TypeVar("T")

'''
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
'''


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

@plugin.include
@arc.slash_command("class", "Get information about a class.")
async def get_class(
    ctx: arc.GatewayContext,
    class_path: arc.Option[str, arc.StrParams(description="The class", name="class", choices=CLASS_LIST)],
) -> None:
    with open(class_path, "r") as file:
        class_json: dict[str, Any] = json.load(file)

    class_json = format_class_data(class_json)

    await ctx.respond(f"```json\n{json.dumps(class_json, indent=2)}```")


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)


@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
