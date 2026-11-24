import json, os, struct, zlib
NS = "qv"
ROOT = os.path.join(os.path.dirname(__file__), "..")
A = os.path.join(ROOT, "src/main/resources/assets", NS)
JAVA = os.path.join(ROOT, "src/main/java/com/example/qv")

# palette: 0 gunmetal 1 steel 2 bright steel 3 black 4 wood 5 red 6 gold 7 blue 8 olive 9 lens 10 tan 11 purple
PAL = ["3a3d42","8e949c","cfd5dc","17181a","7a4a24","c0392b","d4a82b","2c6fbb","5b6b3a","35d0ff","b89a5e","7a3fb0"]

def png(path):
    rows = []
    for y in range(16):
        row = b"\x00"
        for x in range(16):
            if y == 0 and x < len(PAL):
                h = PAL[x]; row += bytes([int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), 255])
            else:
                row += b"\x00\x00\x00\x00"
        rows.append(row)
    raw = b"".join(rows)
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    open(path, "wb").write(data)

def r(x1, y1, x2, y2, c, t=2):
    return ([x1, y1, 8 - t/2], [x2, y2, 8 + t/2], c)

def box(a, b, c, rot=None):
    e = {"from": a, "to": b, "faces": {f: {"uv": [c, 0, c+1, 1], "texture": "#p"}
         for f in ["north","east","south","west","up","down"]}}
    if rot is not None:
        e["rotation"] = {"origin": [8,8,8], "axis": "z", "angle": rot}
    return e

GUNS = {
 "sidearm": ("Sidearm", [r(3,8,13,10.5,1,1.8), r(13,8.6,14,9.9,0,1.0), r(3,7,12,8,0,1.8), r(3,2,5.5,7,3,1.8), r(5.5,5.6,8.5,6.2,0,1.2), r(6,6.2,6.7,7,2,0.6), r(3,10.5,4,11.2,3,1), r(12.5,10.5,13.2,11.2,3,1)]),
 "heavy_pistol": ("Heavy Pistol", [r(2,8,14,11,2,2.2), r(5,11,11,11.5,6,1.2), r(14,8.6,15.5,10.4,0,1.4), r(2,7,11,8,0,2.0), r(2,2,5,7,4,2.0), r(5,5.5,8.5,6.2,0,1.2), r(5.8,6.2,6.6,7,2,0.6), r(2.5,11,3.5,12,3,1), r(13,11,14,12,3,1)]),
 "revolver": ("Revolver", [r(7,9,15,10.8,1,1.6), r(5,8,8,11,0,2.2), r(2,8,6,11,0,1.8), r(2,3,4.5,8,4,1.8), r(1.5,11,2.5,12.2,1,0.8), r(5,6.6,8,7.4,0,1.0), r(14.5,10.8,15.2,11.5,3,0.8)]),
 "machine_pistol": ("Machine Pistol", [r(3,7.5,12,10,3,1.8), r(12,8.2,14.5,9.4,0,1.2), r(14.5,8.1,15.5,9.5,1,1.4), r(7,1.5,9,7.5,0,1.4), r(3,2.5,5.2,7.5,3,1.8), r(5.2,5.8,7,6.4,0,1.0), r(3,10,5,10.8,0,1.0), r(10,10,12,10.8,0,1.0)]),
 "smg": ("SMG", [r(2,7,11,10,0,1.8), r(11,8,14.5,9.4,3,1.4), r(14.5,8.2,15.5,9.2,1,1.0), r(6.5,1,8.5,7,3,1.4), r(3,3,5,7,3,1.8), r(0,8,2,9,1,0.8), r(5.5,6,7,6.7,0,1.0), r(4,10,9,10.8,3,1.0)]),
 "shotgun": ("Pump Shotgun", [r(0,5,3.5,10,4,1.8), r(3.5,7,7.5,10.5,0,1.8), r(7.5,9,16,10.5,1,1.4), r(7.5,7.6,15,8.9,0,1.3), r(9.5,6.8,13,8.4,4,2.0), r(3.5,3.5,5.5,7,3,1.8), r(5.2,6,6.8,6.7,0,1.0), r(15.2,10.5,16,11.2,3,0.8)]),
 "assault_rifle": ("Assault Rifle", [r(0,6,3.5,10,4,1.8), r(3.5,7,10,10.5,0,1.8), r(10,7.5,13.5,10,4,1.8), r(13.5,8.4,16,9.4,1,1.0), r(6.5,3.5,8.5,7,3,1.5), r(6.9,1.8,9.0,3.6,3,1.5), r(3.5,3,5.5,7,3,1.8), r(5.5,6,7,6.7,0,1.0), r(5,10.5,9,11.3,3,1.0), r(13,10,13.8,11.4,3,0.8)]),
 "carbine": ("Carbine", [r(0,6.5,3,9.5,8,1.6), r(3,7,9.5,10,0,1.6), r(9.5,7.6,13,9.6,8,1.6), r(13,8.3,15.5,9.3,1,0.9), r(6,3.5,8,7,3,1.4), r(3,3.5,5,7,3,1.6), r(5,6,6.5,6.7,0,1.0), r(4,10,9,10.8,3,0.9), r(14.5,9.3,15.2,10.5,3,0.7)]),
 "battle_rifle": ("Battle Rifle", [r(0,5.5,4,10,10,2), r(4,7,11,10.5,0,2), r(11,7.5,14,10,10,2), r(14,8.3,16,9.5,1,1.1), r(6,3,8.5,7,3,1.6), r(4,3,5.8,7,10,1.8), r(5.8,6,7.5,6.7,0,1.0), r(5,10.5,10,12,3,1.4), r(4.6,10.8,5,11.7,9,1.1), r(10,10.8,10.4,11.7,9,1.1), r(6,10.2,7,10.5,0,0.8), r(8.5,10.2,9.5,10.5,0,0.8)]),
 "bolt_sniper": ("Bolt Sniper", [r(0,5,5,9.5,4,1.8), r(5,7.5,9,10,0,1.8), r(9,8.2,16,9.4,3,1.0), r(5.5,10.4,12.5,12.2,3,1.8), r(5,10.7,5.5,11.9,9,1.4), r(12.5,10.7,13,11.9,9,1.4), r(6.2,10,7.2,10.4,0,0.8), r(10.8,10,11.8,10.4,0,0.8), r(6,5.5,8,7.5,3,1.4), r(4,3,6,7.5,4,1.6), ([5.8,8.6,8.8],[6.6,9.2,10.2],1), ([5.8,8.4,10.0],[6.6,9.4,10.8],3), r(15.5,7.9,16,9.7,0,1.4)]),
 "heavy_sniper": ("Heavy Sniper", [r(0,5,4,10.5,0,2.4), r(4,7,10,10.5,8,2.6), r(10,8,16,10,3,1.6), r(15,7.2,16,10.8,0,2.2), r(4.5,10.5,13,12.8,3,2.2), r(4,10.8,4.5,12.5,9,1.8), r(13,10.8,13.5,12.5,9,1.8), r(5.5,10.1,6.7,10.5,0,1.0), r(11,10.1,12.2,10.5,0,1.0), r(6,4,9,7,3,1.6), r(3.5,3,5.5,7,3,1.8), r(11,5.5,11.8,8,1,0.6), r(13,5.5,13.8,8,1,0.6)]),
 "auto_sniper": ("Auto Sniper", [r(0,6,4,10,3,1.8), r(4,7,10.5,10.5,0,1.8), r(10.5,8,16,9.6,1,1.2), r(4.5,10.5,11,12.2,3,1.6), r(4,10.8,4.5,12,9,1.2), r(11,10.8,11.5,12,9,1.2), r(5.5,10.2,6.5,10.5,0,0.8), r(9,10.2,10,10.5,0,0.8), r(6.5,2,8.5,7,3,1.6), r(3.5,3,5.5,7,3,1.8), r(5.5,6,7,6.7,0,1.0), r(15.5,7.6,16,10,0,1.4)]),
 "marksman_rifle": ("Marksman Rifle", [r(0,5.5,4.5,9.5,4,1.8), r(4.5,7,10,10,0,1.8), r(10,7.6,14,9.8,4,1.8), r(14,8.3,16,9.5,3,1.0), r(4.5,10,9,11.4,3,1.4), r(4.2,10.3,4.5,11.1,9,1.0), r(9,10.3,9.3,11.1,9,1.0), r(6,3,8,7,3,1.4), r(3.5,3.2,5.5,7,4,1.8), r(5.5,6,7,6.7,0,1.0)]),
}

KNIVES = {
 "combat_knife": ("Combat Knife", [r(7,1,9,5,3,1.6), r(6.6,0,9.4,1,0,1.8), r(6,5,10,6,0,1.6), r(7,6,9.2,12,2,0.8), r(7.3,12,8.9,13.5,2,0.7), r(7.7,13.5,8.5,14.5,2,0.5)]),
 "curved_knife": ("Curved Knife", [r(6,0,10,0.8,3,1.2), r(5.6,0,6.4,2.6,3,1.2), r(9.6,0,10.4,2.6,3,1.2), r(7,1,9,5,3,1.6), r(7,5,9,6,0,1.6), r(7.2,6,9.2,9,1,0.7), r(7.8,9,9.8,11,1,0.7), r(8.6,11,10.4,12.6,1,0.6), r(9.6,12.4,10.8,13.6,2,0.5), r(10.2,13.4,10.8,14.2,2,0.4)]),
 "butterfly_knife": ("Butterfly Knife", [r(5.8,0,7.4,6,3,1.4), r(8.6,0,10.2,6,5,1.4), r(7.4,1,8.6,2,0,1.0), r(7.4,5,8.6,6,0,1.0), r(7.2,6,8.8,12,2,0.6), r(7.4,12,8.6,13.6,2,0.5), r(7.7,13.6,8.3,14.6,2,0.4)]),
 "dagger": ("Dagger", [r(7,0.5,9,5,4,1.6), r(6.6,0,9.4,0.5,6,1.8), r(5,5,11,6,6,1.8), r(7.3,6,8.7,12,2,0.9), r(7.6,12,8.4,13.5,2,0.7), r(7.9,13.5,8.1,14.8,2,0.4), r(7.8,6,8.2,12.8,1,1.1)]),
 "tanto": ("Tanto", [r(7,0.5,9,5,3,1.6), r(6.5,0,9.5,0.5,0,1.8), r(6,5,10,5.8,0,1.8), r(7,5.8,9.2,11,2,0.8), r(7.4,11,9.2,12.4,2,0.7), r(8,12.4,9.2,13.6,2,0.6), r(8.8,13.4,9.2,14.2,2,0.4)]),
 "machete": ("Machete", [r(7,0,9,4.5,4,1.8), r(6.5,4.5,9.5,5.2,0,1.8), r(6.8,5.2,10.2,13,1,0.8), r(7,13,10.6,14.6,2,0.7), r(7.6,14.6,10.8,15.4,2,0.5)]),
}

GUN_DISPLAY = {
 "thirdperson_righthand": {"rotation": [0,-90,0], "translation": [0,3,1], "scale": [0.85,0.85,0.85]},
 "firstperson_righthand": {"rotation": [0,-90,0], "translation": [1.1,2.5,1.1], "scale": [0.8,0.8,0.8]},
 "firstperson_lefthand":  {"rotation": [0,90,0],  "translation": [1.1,2.5,1.1], "scale": [0.8,0.8,0.8]},
 "gui": {"rotation": [0,0,0], "translation": [0,0,0], "scale": [1.0,1.0,1.0]},
 "ground": {"rotation": [0,0,0], "translation": [0,2,0], "scale": [0.5,0.5,0.5]},
 "fixed": {"rotation": [0,0,0], "translation": [0,0,0], "scale": [1.0,1.0,1.0]},
}
KNIFE_DISPLAY = {
 "thirdperson_righthand": {"rotation": [0,-90,55], "translation": [0,4,0.5], "scale": [0.85,0.85,0.85]},
 "firstperson_righthand": {"rotation": [0,-90,25], "translation": [1.13,3.2,1.13], "scale": [0.68,0.68,0.68]},
 "firstperson_lefthand":  {"rotation": [0,90,-25], "translation": [1.13,3.2,1.13], "scale": [0.68,0.68,0.68]},
 "gui": {"rotation": [0,0,0], "translation": [0,0,0], "scale": [1.0,1.0,1.0]},
 "ground": {"rotation": [0,0,0], "translation": [0,2,0], "scale": [0.5,0.5,0.5]},
 "fixed": {"rotation": [0,0,0], "translation": [0,0,0], "scale": [1.0,1.0,1.0]},
}

os.makedirs(os.path.join(A, "models/item"), exist_ok=True)
os.makedirs(os.path.join(A, "items"), exist_ok=True)
os.makedirs(os.path.join(A, "textures/item"), exist_ok=True)
os.makedirs(os.path.join(A, "lang"), exist_ok=True)
png(os.path.join(A, "textures/item/palette.png"))

lang = {
  "key.qv.nametags": "Toggle Nametags",
  "key.qv.menu": "Open QV Menu",
  "key.category.qv.main": "QV",
}
ids = []
for table, display, rot in ((GUNS, GUN_DISPLAY, None), (KNIVES, KNIFE_DISPLAY, -45)):
    for iid, (name, cubes) in table.items():
        model = {
            "textures": {"p": f"{NS}:item/palette", "particle": f"{NS}:item/palette"},
            "gui_light": "front",
            "elements": [box(a, b, c, rot) for (a, b, c) in cubes],
            "display": display,
        }
        json.dump(model, open(os.path.join(A, f"models/item/{iid}.json"), "w"), indent=1)
        json.dump({"model": {"type": "minecraft:model", "model": f"{NS}:item/{iid}"}},
                  open(os.path.join(A, f"items/{iid}.json"), "w"), indent=1)
        lang[f"item.{NS}.{iid}"] = name
        ids.append(iid)

json.dump(lang, open(os.path.join(A, "lang/en_us.json"), "w"), indent=2)
arr = ", ".join(f'"{i}"' for i in ids)
open(os.path.join(JAVA, "QvItems.java"), "w").write(f'''package com.example.qv;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;

public final class QvItems {{
    public static final String[] IDS = {{ {arr} }};
    public static final List<Item> ALL = new ArrayList<>();

    public static void register() {{
        for (String name : IDS) {{
            Identifier id = Identifier.fromNamespaceAndPath(QvMod.MOD_ID, name);
            ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id);
            Item item = new Item(new Item.Properties().setId(key).stacksTo(1));
            Registry.register(BuiltInRegistries.ITEM, key, item);
            ALL.add(item);
        }}
    }}
}}
''')
print("generated", len(ids), "items")
