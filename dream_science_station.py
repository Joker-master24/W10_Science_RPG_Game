import bpy
import math
from mathutils import Vector

# Procedural, original child-friendly dream-lab set for the Godot learning game.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.materials, bpy.data.curves, bpy.data.meshes, bpy.data.cameras, bpy.data.lights):
    pass

def mat(name, color, metallic=0.0, rough=0.45, emission=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = rough
    if emission:
        p.inputs['Emission Color'].default_value = (*color, 1)
        p.inputs['Emission Strength'].default_value = emission
    return m

navy = mat('午夜藍・牆面', (0.025, 0.055, 0.12), rough=.7)
floor_mat = mat('深海藍・地板', (.075, .12, .20), metallic=.3)
gold = mat('星光黃銅', (.95, .57, .19), metallic=.72, rough=.24)
teal = mat('薄荷琉璃', (.08, .72, .60), metallic=.15, emission=.4)
coral = mat('珊瑚紅', (.92, .27, .34), rough=.38)
blueglass = mat('夢境藍玻璃', (.14, .34, .58), metallic=.25, emission=.22)
steel = mat('小船鍍鋅鐵', (.48, .62, .69), metallic=.78, rough=.28)
lemon = mat('檸檬黃', (1.0, .72, .08), rough=.3)
apple = mat('蘋果紅', (.78, .08, .12), rough=.27)
leaf = mat('嫩葉綠', (.14, .46, .19), rough=.4)
white = mat('奶霜陶瓷', (.88, .85, .72), rough=.28)

def cube(name, loc, scale, material, bevel=.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new('柔和倒角','BEVEL'); mod.width=bevel; mod.segments=3
        o.modifiers.new('角點柔化','WEIGHTED_NORMAL')
    return o

def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material)
    bpy.ops.object.shade_smooth(); return o

def cyl(name, loc, radius, depth, material, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(material)
    bevel=o.modifiers.new('倒圓角','BEVEL'); bevel.width=.045; bevel.segments=3
    o.modifiers.new('加權法線','WEIGHTED_NORMAL'); return o

# Room shell and a warm floating exhibition floor.
cube('夢境實驗室地台',(0,0,-.32),(22,15,.58),floor_mat,.2)
cube('背牆',(0,6.9,5.1),(22,.5,10.5),navy,.16)
cube('左側牆',(-10.8,0,5),(0.5,14,10),navy,.14)
cube('右側牆',(10.8,0,5),(.5,14,10),navy,.14)
for x in (-8,-4,0,4,8):
    cube('窗格琉璃',(x,6.57,5.35),(2.65,.12,6.5),blueglass,.32)
    cube('窗格直框',(x-1.38,6.42,5.35),(.09,.2,6.9),gold,.035)
    cube('窗格直框',(x+1.38,6.42,5.35),(.09,.2,6.9),gold,.035)
    cube('窗格橫框',(x,6.42,2.0),(2.85,.2,.1),gold,.035)
    cube('窗格橫框',(x,6.42,8.7),(2.85,.2,.1),gold,.035)
    cube('窗格十字',(x,6.4,5.35),(2.65,.22,.075),gold,.025)

# Display plinths: rust lab and food preservation station.
for x, color in [(-6,teal),(0,gold),(6,coral)]:
    cyl('漂浮展示台',(x,0,.42),1.42,.38,gold)
    cyl('發光基座',(x,0,.2),1.26,.12,color)
    cyl('展示柱',(x,0,1.4),.12,1.65,white)
    sphere('星塵燈',(x,0,2.35),(.3,.3,.3),color)

# A stylised riveted iron boat: pointed bow via mesh, safety-colored trim.
verts=[(-1.45,-.3,2.0),(1.25,-.3,2.0),(1.65,-.3,2.26),(-1.45,.3,2.0),(1.25,.3,2.0),(1.65,.3,2.26),(-1.15,-.3,2.75),(1.0,-.3,2.75),(-1.15,.3,2.75),(1.0,.3,2.75)]
faces=[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(0,2,6),(2,7,6),(3,8,9),(3,9,5),(6,7,9,8),(0,6,8,3),(1,4,9,7),(2,5,9,7)]
mesh=bpy.data.meshes.new('小船船殼網格'); mesh.from_pydata(verts,[],faces); mesh.materials.append(steel)
boat=bpy.data.objects.new('守護小船・鐵製模型',mesh); bpy.context.collection.objects.link(boat)
boat.location=(-6,0,0); bevel=boat.modifiers.new('柔化船緣','BEVEL'); bevel.width=.07; bevel.segments=3
cube('船身珊瑚色防護塗層飾帶',(-5.95,-.33,2.3),(2.2,.08,.12),coral,.04)
for x in (-7,-6.4,-5.8,-5.2): sphere('船身鉚釘',(x,-.37,2.55),(.055,.035,.055),gold)
cube('船艙座椅',(-6.1,0,2.82),(.35,.58,.13),gold,.05)

# Rust-learning clue: protected iron nail and a large water droplet.
cyl('乾燥保存的鐵釘',(-6,.02,3.55),.11,1.0,steel,24)
sphere('防鏽水滴模型',(-4.2,0,2.4),(.43,.42,.62),teal)
cube('防鏽漆樣本盒',(-7.4,.15,1.0),(.52,.52,.48),coral,.09)

# Fridge case and preserved picnic foods on the right-hand station.
cube('冷藏櫃外殼',(6,0,2.65),(2.05,1.35,3.4),white,.23)
cube('冷藏櫃冷光門',(6,-.72,2.72),(1.72,.08,2.95),blueglass,.17)
cube('冷藏櫃上層分界',(6,-.79,3.2),(1.65,.07,.07),gold,.025)
cyl('冷藏櫃把手',(6.67,-.87,2.55),.055,.52,gold,24).rotation_euler[1]=math.pi/2
for z in (1.75,2.75,3.65): cube('冰箱層架',(6,-.58,z),(1.46,.5,.06),white,.025)
for x,z,m in [(5.6,1.98,apple),(6.1,1.98,lemon),(5.65,2.98,teal),(6.15,2.98,white)]:
    cyl('密封食品罐',(x,-.42,z),.17,.35,m,32)
    cyl('食品罐密封蓋',(x,-.42,z+.2),.18,.07,gold,32)
sphere('野餐蘋果',(3.7,.0,2.12),(.45,.4,.44),apple)
sphere('蘋果葉',(3.7,0,2.55),(.15,.08,.07),leaf)
sphere('新鮮檸檬',(4.55,.0,2.10),(.52,.32,.30),lemon)
cyl('檸檬汁小杯',(3.9,.1,1.7),.27,.22,teal,40)

# Friendly hooded keeper figurine, with smooth, rounded shapes.
sphere('守護員披風身體',(0,-.2,2.12),(.62,.46,.91),coral)
sphere('守護員小小臉龐',(0,-.54,2.85),(.48,.38,.54),white)
sphere('披風兜帽',(0,-.34,3.16),(.62,.46,.42),gold)
sphere('兜帽陰影',(0,-.745,2.99),(.39,.13,.32),navy)
for x in (-.15,.15): sphere('溫柔眼睛',(x,-.865,2.99),(.045,.035,.052),white)
cube('小小披風尾端',(0,.05,1.45),(.92,.35,.16),gold,.09)

# Floating crystal keys signal unlockable progress.
for x,z,material in [(-1.2,4.0,gold),(1.2,4.0,teal)]:
    bpy.ops.mesh.primitive_torus_add(major_radius=.32,minor_radius=.075,major_segments=40,minor_segments=12,location=(x,-.2,z))
    bpy.context.object.name='鑰匙星環'; bpy.context.object.data.materials.append(material)
    cube('鑰匙齒',(x+.37,-.2,z-.23),(.38,.12,.11),material,.04)

# Soft theatrical lighting and a clean front three-quarter camera.
world=bpy.context.scene.world; world.color=(.055,.075,.13)
def area(name, loc, power, size, color, target):
    bpy.ops.object.light_add(type='AREA', location=loc); l=bpy.context.object; l.name=name
    l.data.energy=power; l.data.shape='DISK'; l.data.size=size; l.data.color=color
    l.rotation_euler=(Vector(target)-l.location).to_track_quat('-Z','Y').to_euler()
area('暖色主光',(-5,-7,10),1500,8,(1,.73,.48),(0,0,1.5))
area('藍色輪廓光',(7,4,8),1900,7,(.35,.62,1),(0,0,2))
area('柔和正面補光',(1,-9,5),1000,7,(.72,.88,1),(0,0,2))
bpy.ops.object.camera_add(location=(13,-22,13))
cam=bpy.context.object; cam.name='夢境科學站展示相機'; cam.rotation_euler=(Vector((0,1.0,3.0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO'; cam.data.ortho_scale=25; bpy.context.scene.camera=cam
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=32
scene.render.resolution_x=1400; scene.render.resolution_y=900; scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG'; scene.render.filepath='//dream_science_station.png'
scene.camera.data.lens=50
# Save next to this script, so it can be run from Blender's background CLI.
import os
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'dream_science_station.blend')
bpy.ops.wm.save_as_mainfile(filepath=out)
print('Saved',out)
