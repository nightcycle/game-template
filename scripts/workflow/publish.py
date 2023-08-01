import sys
import os
import requests
import yaml
import json
from ropublisher import Publisher
from tempfile import TemporaryDirectory
from requests import Session

GROUP_ID = 4181328
UNIVERSE_ID = 4659672329
REPO_OWNER = "nightcycle"
REPO_NAME = "wasteland-engineer"
API_KEY_ID = "35b8179d-889f-4e6b-a4c2-73940408dddc"
API_KEY_NAME = "Wasteland Engineer Publish"

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except requests.RequestException:
        return None

def get_xcrf_token(session: Session) -> str:
	response = session.post("https://auth.roblox.com/v2/logout")
	token = response.headers["x-csrf-token"]
	assert token
	return token

def get_universe_id(session: Session, place_id: int) -> int:
	response = session.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}")
	for place in json.loads(response.text):
		universe_id = int(place["universeId"])
		assert universe_id
		return universe_id
	raise ValueError("Bad response: "+response.text)

with TemporaryDirectory() as temp_dir_path:
	print(f"created temp directory {temp_dir_path}")
	version_text = sys.argv[1]
	access_key = sys.argv[2]
	api_key = sys.argv[3]
	roblox_cookie = sys.argv[4]

	repo_path = f"{REPO_OWNER}/{REPO_NAME}@" + version_text
	if version_text[0].lower() == "v":
		repo_path = f"{REPO_OWNER}/{REPO_NAME}@" + version_text[1:]

	base_path = repo_path.split("@")[0]

	user_name = base_path.split("/")[0]
	repo_name = base_path.split("/")[1]
	release_name = repo_path.split("@")[1]

	print(f"getting release info {repo_path}")
	response = requests.get(
		url = f"https://api.github.com/repos/{user_name}/{repo_name}/releases",
		headers={
			"Authorization": f"Bearer {access_key}",
			"X-GitHub-Api-Version": "2022-11-28",
			"accept": "json",
			"Accept-Encoding": "gzip, deflate, br",
		},
	)
	if not response.status_code == 200:
		raise ValueError(response.content)
	
	release_data_list: list[dict] = json.loads(response.content)
	for release_data in release_data_list:
		tag_name: str = release_data["tag_name"]
		print(f"release name: {tag_name}")
		if (tag_name == release_name or tag_name == "v" + release_name ):
			for asset_data in release_data["assets"]:
				asset_name: str = asset_data["name"]
				print(f"asset name: {asset_name}")
				if os.path.splitext(asset_name)[1] == ".rbxl":
					asset_id = asset_data["id"]
					scene_name = os.path.splitext(asset_data["name"])[0]
					scene_config_path = f"scene/{scene_name}/scene.yaml"

					place_id = -1
					with open(scene_config_path, "r") as scene_file:
						scene_config_data = yaml.safe_load(scene_file.read())
						place_id = scene_config_data["PlaceId"]

					assert place_id > 0

					build_file_name = scene_name+"_"+str(place_id)+".rbxl"
					print(f"downloading {build_file_name}")
					download_response = requests.get(
						url = f"https://api.github.com/repos/{user_name}/{repo_name}/releases/assets/{asset_id}",
						headers={
							"Authorization": f"Bearer {access_key}",
							"X-GitHub-Api-Version": "2022-11-28",
							"accept": "application/octet-stream",
							"Accept-Encoding": "gzip, deflate, br",
						},
					)
					print("download response: ", download_response.status_code, download_response.reason)
					if not download_response.status_code == 200:
						raise ValueError(response.content)
					content = download_response.content
					
					with open(temp_dir_path+"/"+build_file_name, "wb") as out_file:
						out_file.write(content)
			break
	# # update ip address
	# print("updating ip address whitelist")
	# session = requests.Session()
	# session.cookies.update({
	# 	".ROBLOSECURITY": roblox_cookie
	# })
	# session.headers.update({
	# 	"X-Csrf-Token": get_xcrf_token(session),
	# 	"Content-Type": "application/json",
	# 	"Accept-Encoding": "gzip, deflate, br",
	# 	"Accept": "*/*",
	# })

	# ip_address = get_public_ip()
	# assert ip_address != None
	# print("IP", ip_address)
	# response = session.patch(
	# 	url="https://apis.roblox.com/cloud-authentication/v1/apiKey",
	# 	data=json.dumps({
	# 		"cloudAuthId":API_KEY_ID,
	# 		"cloudAuthUserConfiguredProperties":{
	# 			"name":API_KEY_NAME,
	# 			"description":"",
	# 			"isEnabled":True,
	# 			"allowedCidrs":[ip_address],
	# 			"scopes":[
	# 				{
	# 					"scopeType":"universe-places",
	# 					"targetParts":[str(UNIVERSE_ID)],
	# 					"operations":["write"]
	# 				}
	# 			]
	# 		}
	# 	})
	# )
	# print("ip update response", response.status_code, response.reason)
	# assert response.status_code == 200

	publisher = Publisher(
		place_key=api_key,
		group_id=GROUP_ID,
		cookie=roblox_cookie
	)

	for file_path in os.listdir(temp_dir_path):
		print(f"publishing {file_path}")
		place_id = int(os.path.splitext(file_path)[0].split("_")[1])
		full_rbx_path = temp_dir_path + "/" + file_path

		publisher.update_place(
			file_path=full_rbx_path, 
			place_id=place_id
		)
		print(f"publish {file_path} complete")