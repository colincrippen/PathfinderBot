import json
import os

directory_name = "classes"

names: dict[str, str] = {}
for filename in os.listdir(dir_path := f"./pathfinder_bot/data/{directory_name}"):
    with open(full_path := f"{dir_path}/{filename}", "r") as file:
        data = json.loads(file.read())
        # if data.get("system").get("publication").get("remaster"):
        names[name := data.get("name")] = full_path

        # print(f"{name}: {data.get("system")}")

names = dict(sorted(names.items()))

with open(f"{directory_name}_dict.txt", "w") as file:
    file.write(str(names))
print(str(names))
