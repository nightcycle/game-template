import sys
import bpy
import os

def split_blend_by_material(blend_path: str):
	bpy.ops.wm.open_mainfile(filepath =os.path.abspath(blend_path))
	bpy.ops.mesh.separate(type='MATERIAL')

	out_dir_path = os.path.split(blend_path)[0]
	if not os.path.exists(out_dir_path):
		os.makedirs(out_dir_path)

	for mesh in bpy.data.objects:
		if mesh.type == 'MESH':
			bpy.ops.object.select_all(action='DESELECT')
			assert len(mesh.material_slots) <= 1, f"separate failed: {len(mesh.material_slots)} for {mesh.name}"
			if len(mesh.material_slots) > 0:
				mesh_name = mesh.name
				material = mesh.material_slots[0]
				material_name = material.name
				mesh_base = os.path.splitext(mesh_name)[0]
				bpy.context.view_layer.objects.active = mesh
				mesh.select_set(True)
				out_path_base = out_dir_path+"/"+mesh_base+"_"+material_name
				bpy.ops.export_scene.obj(filepath=out_path_base+".obj", 
					check_existing=True, 
					filter_glob="*.obj;*.mtl", 
					use_selection=True
				)
				if os.path.exists(out_path_base+".mtl"):
					os.remove(out_path_base+".mtl")

def split_directory(dir_path: str):
	for file_name in os.listdir(dir_path):
		full_path = dir_path+"/"+file_name
		base, ext = os.path.splitext(full_path)
		if ext == ".blend":
			split_blend_by_material(full_path)

split_directory(sys.argv[1])	
