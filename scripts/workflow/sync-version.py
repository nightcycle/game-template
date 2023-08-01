import sys
import toml
import yaml
import json
import os
import re

VERSION_ID = sys.argv[1]
CLEAN_VERSION_ID = re.sub('[a-zA-Z]', '', VERSION_ID)
VERSION_PARTS = CLEAN_VERSION_ID.split(".")
assert(len(VERSION_PARTS) == 3)

MAJOR = int(VERSION_PARTS[0])
MINOR = int(VERSION_PARTS[1])
PATCH = int(VERSION_PARTS[2])

# update wally
WALLY_TOML_PATH = "wally.toml"
wally_config = toml.load(WALLY_TOML_PATH)
wally_config["version"] = CLEAN_VERSION_ID
with open(WALLY_TOML_PATH, "w") as wally_file:
    wally_file.write(toml.dumps(wally_config))

# update midas
MIDAS_YAML_PATH = "midas.yaml"
with open(MIDAS_YAML_PATH, "r") as midas_read_file:
	midas_config = yaml.safe_load(midas_read_file.read())
	midas_config["version"]["major"] = MAJOR
	midas_config["version"]["minor"] = MINOR
	midas_config["version"]["patch"] = PATCH
	if "hotfix" in midas_config["version"]:
		midas_config["version"].pop("hotfix")
	with open(MIDAS_YAML_PATH, "w") as midas_file:
		midas_file.write(yaml.safe_dump(midas_config))

# update rojo
ROJO_PATH = "default.project.json"
with open(ROJO_PATH, "r") as rojo_read_file:
	rojo_data = json.loads(rojo_read_file.read())
	rojo_data["name"] = str(rojo_data["name"]).split("@")[0] + "@" + CLEAN_VERSION_ID
	with open(ROJO_PATH, "w") as rojo_write_file:
		rojo_write_file.write(json.dumps(rojo_data, indent=5))

# luau version file
LUAU_OUT_DIR = "out/Shared"
LUAU_PATH = LUAU_OUT_DIR + "/Version.luau"

if not os.path.exists(LUAU_OUT_DIR):
	os.makedirs(LUAU_OUT_DIR)

with open(LUAU_PATH, "w") as luau_write_file:
	luau_write_file.write(f"--!strict\nreturn \"{MAJOR}.{MINOR}.{PATCH}\"")
