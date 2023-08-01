import os
import time
import json
from luau import path as luau_path
from typing import Any

def measure_script_duration(path: str) -> float:
	current_tick = time.time()
	print("measuring", path)
	os.system(f"luau-lsp analyze {path} --sourcemap=sourcemap.json --ignore=\"*.spec.luau\" --ignore=\"*.spec.lua\" --flag:LuauTypeInferIterationLimit=0 --flag:LuauCheckRecursionLimit=0 --flag:LuauTypeInferRecursionLimit=0 --flag:LuauTarjanChildLimit=0 --flag:LuauTypeInferTypePackLoopLimit=0 --flag:LuauVisitRecursionLimit=0 --definitions=types/globalTypes.d.lua")
	duration = time.time() - current_tick
	return duration

def iterate_files(dir_path: str) -> dict[str, float]:
	duration_registry = {}
	for root, dirs, files in os.walk(dir_path):
		for filename in files:
			file_path = os.path.join(root, filename)
			file_ext = os.path.splitext(file_path)[1]
			if file_ext == ".luau" or file_ext == ".lua":
				duration_registry[file_path] = measure_script_duration(file_path)

	return duration_registry

with open("lsp-duration.json", "w") as out_file:
	src_registry = iterate_files("src")
	# package_registry= iterate_files("Packages")
	# out_registry = iterate_files("out")
	registry: dict[str, float] = {}
	registry.update(src_registry)
	# registry.update(package_registry)
	# registry.update(out_registry)
	
	total_duration = 0.0
	entry_count = 0
	for k, v in registry.items():
		total_duration += v
		entry_count += 1
	
	average_entry_duration = total_duration/entry_count

	final_list = []
	for k, v in registry.items():
		final_list.append({
			"path": k.replace("\\", "/"),
			"duration": v,
			"avg": average_entry_duration,
			"score": v/average_entry_duration,
		})
	sorted_data = sorted(final_list, key=lambda x: x['score'], reverse=True)
	out_file.write(json.dumps(sorted_data, indent=5))